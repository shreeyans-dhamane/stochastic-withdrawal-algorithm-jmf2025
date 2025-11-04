suppressPackageStartupMessages(library(optparse))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(scales))

option_list <- list(
  make_option(c("-i", "--input"), type="character", default=NULL,
              help="Path to the input CSV file (simulation_results.csv)", metavar="FILE"),
  make_option(c("-o", "--output"), type="character", default="simulation_plot.tiff",
              help="Path to the output TIFF file [default= %default]", metavar="FILE"),
  make_option(c("-p", "--percentile"), type="numeric", default=NULL,
              help="The percentile t-value to mark with a vertical line", metavar="VALUE")
)

parser <- OptionParser(option_list=option_list)
args <- parse_args(parser)

if (is.null(args$input)) {
  print_help(parser)
  stop("Input file argument (--input) is required.", call.=FALSE)
}

tryCatch({
  sim_data <- read_csv(args$input, col_types = cols(t_value = "d"))
}, error = function(e) {
  stop(paste("Error reading input file:", e$message), call.=FALSE)
})

if (nrow(sim_data) == 0) {
  stop("Input CSV file is empty. Cannot generate plot.", call.=FALSE)
}

plot_title <- "Distribution of Fund Longevity (t-values)"
percentile_label <- if (!is.null(args$percentile)) paste0(round(args$percentile, 1), " months") else ""

p <- ggplot(sim_data, aes(x = t_value)) +
  geom_histogram(binwidth = 5, fill = "#C00000", color = "#8F0000", alpha = 0.8) +
  
  {
    if (!is.null(args$percentile)) {
      list(
        geom_vline(
          xintercept = args$percentile,
          color = "blue",
          linetype = "dashed",
          size = 1
        ),
        annotate(
          "text",
          x = args$percentile,
          y = Inf,
          label = percentile_label,
          vjust = 2,
          hjust = -0.1,
          color = "blue",
          angle = 90
        )
      )
    }
  } +
  
  scale_x_continuous(labels = comma) +
  scale_y_continuous(labels = comma) +
  labs(
    title = plot_title,
    x = "Fund Longevity (Months)",
    y = "Frequency"
  ) +
  theme_minimal(base_family = "sans") +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    panel.grid.minor = element_blank()
  )

tryCatch({
  ggsave(
    args$output,
    plot = p,
    device = "tiff",
    width = 10,
    height = 6,
    units = "in",
    dpi = 300,
    compression = "lzw"
  )
  cat(paste("Plot successfully saved to", args$output, "\n"))
}, error = function(e) {
  stop(paste("Error saving plot:", e$message), call.=FALSE)
})
