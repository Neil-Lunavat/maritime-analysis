library(tidyverse)
library(readr)
library(ggcorrplot)
library(scales)
library(gridExtra)

dir.create("plots", showWarnings = FALSE)

df <- read_csv('20251007_092747.csv')

type_mapping <- df %>%
  filter(!is.na(SHIPTYPE) & !is.na(TYPE_NAME)) %>%
  group_by(SHIPTYPE) %>%
  summarize(TYPE_NAME = first(TYPE_NAME))
df <- df %>%
  left_join(type_mapping %>% rename(TYPE_NAME_NEW = TYPE_NAME), by = "SHIPTYPE") %>%
  mutate(TYPE_NAME = ifelse(is.na(TYPE_NAME), TYPE_NAME_NEW, TYPE_NAME)) %>%
  select(-TYPE_NAME_NEW)

df <- df %>% select(-SHIPTYPE, -TYPE_IMG)
df <- df %>% rename(SHIPTYPE = TYPE_NAME)

png("plots/01_speed_distribution.png", width=2400, height=1600, res=150)
par(mfrow=c(1,2))
hist(df$SPEED, breaks=50, main="Speed Distribution - All Vessels",
     xlab="Speed (knots)", col="steelblue", border="white")
hist(df$SPEED[df$SPEED > 0], breaks=50, main="Speed Distribution - Moving Vessels Only",
     xlab="Speed (knots)", col="coral", border="white")
par(mfrow=c(1,1))
dev.off()

both <- df %>%
  filter(!is.na(HEADING) & !is.na(COURSE))

both <- both %>%
  mutate(
    HC_DIFF = ifelse(
      abs(HEADING - COURSE) <= 180,
      HEADING - COURSE,
      ifelse(
        HEADING - COURSE > 180,
        HEADING - COURSE - 360,
        HEADING - COURSE + 360
      )
    ),
    HC_DIFF_ABS = abs(HC_DIFF)
  )

threshold <- 90
normal <- both %>% filter(HC_DIFF_ABS <= threshold)
anomalous <- both %>% filter(HC_DIFF_ABS > threshold & SPEED > 10)

p2 <- ggplot() +
  geom_point(data=normal, aes(x=LENGTH, y=SPEED), alpha=0.5, color='steelblue', size=2) +
  geom_point(data=anomalous, aes(x=LENGTH, y=SPEED), alpha=0.8, color='red',
             size=3, shape=17) +
  labs(x="Vessel Length (meters)", y="Speed (knots)",
       title="Heading-Course Misalignment Analysis",
       subtitle=paste0("Red triangles: Angular difference >90° at speed >10 knots (n=",
                      nrow(anomalous), ")")) +
  theme_minimal(base_size=14) +
  theme(panel.grid = element_line(),
        plot.title = element_text(face="bold"))
ggsave("plots/02_hc_diff_anomalies.png", p2, width=10, height=6, dpi=150)

valid_lw <- df %>%
  filter(!is.na(LENGTH) & !is.na(WIDTH) & WIDTH > 0) %>%
  mutate(LW_RATIO = LENGTH / WIDTH)

df <- df %>%
  left_join(valid_lw %>% select(SHIP_ID, LW_RATIO), by = "SHIP_ID")

lw_summary <- df %>%
  filter(!is.na(SHIPTYPE) & !is.na(LW_RATIO)) %>%
  group_by(SHIPTYPE) %>%
  filter(n() >= 50) %>%
  ungroup()

p3 <- ggplot(lw_summary, aes(x=reorder(SHIPTYPE, LW_RATIO, FUN=median),
                              y=LW_RATIO, fill=SHIPTYPE)) +
  geom_boxplot(alpha=0.7, outlier.alpha=0.3) +
  coord_flip() +
  labs(x="", y="Length-to-Width Ratio",
       title="Vessel Proportions by Ship Type",
       subtitle="Higher ratio indicates narrower vessels relative to length") +
  theme_minimal(base_size=14) +
  theme(legend.position = "none",
        plot.title = element_text(face="bold"))
ggsave("plots/03_lw_ratio_by_shiptype.png", p3, width=10, height=7, dpi=150)

p4 <- df %>%
  filter(!is.na(DWT) & !is.na(LENGTH) & !is.na(SHIPTYPE) & DWT > 0) %>%
  ggplot(aes(x=LENGTH, y=DWT, color=SHIPTYPE)) +
  geom_point(alpha=0.6, size=2.5) +
  scale_y_log10(labels=comma) +
  labs(x="Vessel Length (meters)", y="Deadweight Tonnage (log scale)",
       title="Vessel Dimensions and Cargo Capacity by Type",
       color="Vessel Type") +
  theme_minimal(base_size=14) +
  theme(legend.position = "right",
        panel.grid = element_line(),
        plot.title = element_text(face="bold"))
ggsave("plots/04_dwt_vs_length.png", p4, width=11, height=6, dpi=150)

df <- df %>% select(-ELAPSED)

p5 <- df %>%
  ggplot(aes(x=LON, y=LAT)) +
  geom_point(alpha=0.15, color='navy', size=1) +
  labs(x="Longitude", y="Latitude",
       title="Global Distribution of Marine Vessels",
       subtitle="Snapshot of 10,379 vessels from MarineTraffic API") +
  theme_minimal(base_size=14) +
  theme(plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="aliceblue"))
ggsave("plots/05_geographic_distribution.png", p5, width=12, height=7, dpi=150)

p6 <- df %>%
  filter(!is.na(SPEED)) %>%
  ggplot(aes(x=LON, y=LAT, color=SPEED)) +
  geom_point(alpha=0.4, size=1.5) +
  scale_color_viridis_c(option="plasma",
                        limits=c(0, quantile(df$SPEED, 0.999, na.rm=TRUE))) +
  labs(x="Longitude", y="Latitude",
       title="Vessel Speed Distribution by Geographic Location",
       color="Speed\n(knots)") +
  theme_minimal(base_size=14) +
  theme(plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="gray95"),
        legend.position = "right")
ggsave("plots/06_speed_by_location.png", p6, width=12, height=7, dpi=150)

numeric_cols <- c('LAT', 'LON', 'SPEED', 'COURSE', 'HEADING', 'LENGTH',
                  'WIDTH', 'DWT', 'ROT', 'LW_RATIO')
corr_matrix <- df %>%
  select(all_of(numeric_cols)) %>%
  cor(use="complete.obs")

p7 <- ggcorrplot(corr_matrix, hc.order=FALSE, type="full", lab=TRUE,
           lab_size=3.5, colors=c("#6D9EC1", "white", "#E46726"),
           title="Correlation Matrix of Vessel Features",
           legend.title="Pearson\nCorrelation") +
  theme(plot.title = element_text(face="bold", size=16))
ggsave("plots/07_correlation_matrix.png", p7, width=10, height=8, dpi=150)

png("plots/08_missing_data_analysis.png", width=2400, height=1600, res=150)
missing_pct <- (colSums(is.na(df)) / nrow(df)) * 100
missing_df <- data.frame(
  Feature = names(missing_pct),
  Percentage = missing_pct
) %>% filter(Percentage > 0) %>% arrange(desc(Percentage))

barplot(missing_df$Percentage, names.arg=missing_df$Feature,
        main="Missing Data Distribution Across Features",
        ylab="Percentage Missing (%)", xlab="Feature",
        col="indianred", las=2, cex.names=0.8)
abline(h=50, lty=2, col="darkred", lwd=2)
dev.off()

lm_data <- df %>%
  filter(!is.na(LENGTH) & !is.na(WIDTH) & WIDTH > 0)

model <- lm(WIDTH ~ LENGTH, data=lm_data)

p9 <- ggplot(lm_data, aes(x=LENGTH, y=WIDTH)) +
  geom_point(alpha=0.3, color='steelblue', size=2) +
  geom_smooth(method='lm', color='red', se=TRUE, linewidth=1.2, alpha=0.2) +
  labs(x="Vessel Length (meters)", y="Vessel Width (meters)",
       title="Simple Linear Regression: Vessel Width ~ Length",
       subtitle=paste0("R² = ", round(summary(model)$r.squared, 4),
                      " | Coefficient = ", round(coef(model)[2], 4),
                      " | p < 2.2e-16")) +
  theme_minimal(base_size=14) +
  theme(plot.title = element_text(face="bold"),
        plot.subtitle = element_text(size=11, color="gray30"))
ggsave("plots/09_regression_basic.png", p9, width=10, height=7, dpi=150)

lm_data_with_type <- lm_data %>%
  filter(!is.na(SHIPTYPE))

p10 <- ggplot(lm_data_with_type, aes(x=LENGTH, y=WIDTH)) +
  geom_point(aes(color=SHIPTYPE), alpha=0.6, size=2.5) +
  geom_smooth(method='lm', color='black', se=TRUE, linewidth=1.2, alpha=0.15) +
  scale_color_brewer(palette="Set2") +
  labs(x="Vessel Length (meters)", y="Vessel Width (meters)",
       title="Dimensional Relationships Stratified by Vessel Type",
       subtitle=paste0("Overall linear fit: WIDTH = ", round(coef(model)[1], 2),
                      " + ", round(coef(model)[2], 4), " × LENGTH"),
       color="Vessel Type") +
  theme_minimal(base_size=14) +
  theme(
    legend.position = "bottom",
    plot.title = element_text(size=15, face="bold"),
    plot.subtitle = element_text(size=10, color="gray30")
  ) +
  guides(color = guide_legend(nrow=2, override.aes = list(size=4, alpha=1)))
ggsave("plots/10_regression_by_shiptype.png", p10, width=11, height=8, dpi=150)

png("plots/11_regression_diagnostics.png", width=2400, height=2400, res=150)
par(mfrow=c(2,2))
plot(model, which=1:4, pch=20, col=rgb(0,0,1,0.3))
par(mfrow=c(1,1))
dev.off()

lm_data_3d <- lm_data %>%
  filter(!is.na(SPEED) & !is.na(SHIPTYPE))

p12 <- ggplot(lm_data_3d, aes(x=LENGTH, y=WIDTH)) +
  geom_point(aes(color=SHIPTYPE, size=SPEED), alpha=0.6) +
  geom_smooth(method='lm', color='black', se=FALSE, linewidth=1) +
  scale_size_continuous(range=c(1, 10)) +
  scale_color_brewer(palette="Dark2") +
  labs(x="Vessel Length (meters)", y="Vessel Width (meters)",
       title="Multivariate Visualization: Dimensions and Operational Speed",
       subtitle="Point size represents vessel speed; larger points indicate faster vessels",
       color="Vessel Type", size="Speed (knots)") +
  theme_minimal(base_size=14) +
  theme(legend.position = "right",
        plot.title = element_text(face="bold"))
ggsave("plots/12_dimensions_with_speed.png", p12, width=12, height=7, dpi=150)

cat("\n✓ Successfully exported 12 plots to 'plots/' directory\n\n")
cat("Generated files:\n")
cat("  01_speed_distribution.png\n")
cat("  02_hc_diff_anomalies.png\n")
cat("  03_lw_ratio_by_shiptype.png\n")
cat("  04_dwt_vs_length.png\n")
cat("  05_geographic_distribution.png\n")
cat("  06_speed_by_location.png\n")
cat("  07_correlation_matrix.png\n")
cat("  08_missing_data_analysis.png\n")
cat("  09_regression_basic.png\n")
cat("  10_regression_by_shiptype.png\n")
cat("  11_regression_diagnostics.png\n")
cat("  12_dimensions_with_speed.png\n")
