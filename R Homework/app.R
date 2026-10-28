library(shiny)
library(ggplot2)
library(plotly)
library(dplyr)
library(readr)

# load in the dataset and filter for just south carolina
schools <- read.csv("RHW_Public_School_Characteristics_2022-23.csv")
sc_schools <- subset(schools, STABR == "SC")

ui <- fluidPage(
  titlePanel("R Homework Assignment"),
  
  sidebarLayout(
    sidebarPanel(
      p("These visualizations are based public school data downloaded from data.gov"),
      tags$a(href = "https://catalog.data.gov/dataset/public-school-characteristics-2022-23", 
             "click to visit", target = "_blank"),
      br(), br(),
      
      # drop down for school level
      selectInput("school_level", "School Level", 
                  choices = c("All", sort(unique(na.omit(sc_schools$SCHOOL_LEVEL)))),
                  selected = "All"),
      
      # text box for city search
      textInput("city", "City", value = "")
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Enrollment by FTE", plotlyOutput("scatter")),
        tabPanel("Student Faculty Ratio", plotlyOutput("box")),
        tabPanel("School Types", plotlyOutput("bar"))
      )
    )
  )
)

server <- function(input, output) {
  
  # reactive dataset that updates when user changes filters
  my_data <- reactive({
    df <- sc_schools
    
    if (input$school_level != "All") {
      df <- df[df$SCHOOL_LEVEL == input$school_level, ]
    }
    
    if (input$city != "") {
      df <- df[grepl(input$city, df$LCITY, ignore.case = TRUE), ]
    }
    
    return(df)
  })
  
  # first viz: scatter plot
  output$scatter <- renderPlotly({
    p <- ggplot(my_data(), aes(x = TOTAL, y = FTE, color = SCHOOL_LEVEL, 
                               text = paste0(SCH_NAME, "\nTotal: ", TOTAL, "\nFTE: ", FTE))) +
      geom_point() +
      labs(x = "Students", y = "FTE", color = "School Level")
    
    ggplotly(p, tooltip = "text")
  })
  
  # second viz: box plots
  output$box <- renderPlotly({
    p <- ggplot(my_data(), aes(x = SCHOOL_TYPE_TEXT, y = STUTERATIO)) +
      geom_boxplot() +
      labs(x = "School Type", y = "Student Faculty Ratio")
    
    ggplotly(p)
  })
  
  # third viz: bar chart
  output$bar <- renderPlotly({
    p <- ggplot(my_data(), aes(x = VIRTUAL, y = TOTAL, fill = SCHOOL_TYPE_TEXT,
                               text = paste(SCH_NAME, TOTAL))) +
      geom_col() +
      labs(x = "", y = "Students", fill = "Type")
    
    ggplotly(p, tooltip = "text")
  })
}

shinyApp(ui = ui, server = server)