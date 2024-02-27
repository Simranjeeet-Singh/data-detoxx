resource "aws_cloudwatch_log_metric_filter" "syntax_error" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group ]
  name           = "SyntaxMetricLog"
  pattern        = "SyntaxError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_file_reader.function_name}"
  metric_transformation {
    name      = "SyntaxErrorCount"
    namespace = "LogMetric"
    value     = "1"
  }
}
resource "aws_cloudwatch_log_metric_filter" "Runtime-Error" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group ]
  name           = "RuntimeErrorLog"
  pattern        = "RuntimeError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_file_reader.function_name}"
  metric_transformation {
    name      = "RunTimeErrorCount"
    namespace = "LogMetric"
    value     = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "value_error" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group ]
  name           = "ValueMetricLog"
  pattern        = "ValueError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_file_reader.function_name}"
  metric_transformation {
    name      = "ValueErrorCount"
    namespace = "LogMetric"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda-syntax-error-alarm" {
  alarm_name                = "lambda-syntax-error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "SyntaxErrorCount"
  namespace                 = "LogMetric"
  period                    = 300
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for syntax errors from lambda1"
  alarm_actions             = [aws_sns_topic.error_alerts.arn]
  insufficient_data_actions = []
}
resource "aws_cloudwatch_metric_alarm" "lambda-Runtime-Error-alarm" {
  alarm_name                = "lambda-Runtime-Error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "RunTimeErrorCount"
  namespace                 = "LogMetric"
  period                    = 300
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for runtime errors from lambda1"
  alarm_actions             = [aws_sns_topic.error_alerts.arn]
  insufficient_data_actions = []
}

resource "aws_cloudwatch_metric_alarm" "lambda-value-error-alarm" {
  alarm_name                = "lambda-value-error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "ValueErrorCount"
  namespace                 = "LogMetric"
  period                    = 300
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for value errors from lambda1"
  alarm_actions             = [aws_sns_topic.error_alerts.arn]
  insufficient_data_actions = []
}

resource "aws_sns_topic" "error_alerts" {
  name = "lambda-error-alerts"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.error_alerts.arn
  protocol  = "email"
  endpoint  = "detoxdata7@gmail.com"
}

#Lambda 2
resource "aws_cloudwatch_log_metric_filter" "syntax_error_2" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group_2 ]
  name           = "SyntaxMetricLog_2"
  pattern        = "SyntaxError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_processor.function_name}"
  metric_transformation {
    name      = "SyntaxErrorCount_2"
    namespace = "LogMetric_2"
    value     = "1"
  }
}
resource "aws_cloudwatch_log_metric_filter" "Runtime-Error_2" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group_2 ]
  name           = "RuntimeErrorLog_2"
  pattern        = "RuntimeError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_processor.function_name}"
  metric_transformation {
    name      = "RunTimeErrorCount_2"
    namespace = "LogMetric_2"
    value     = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "value_error_2" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group_2 ]
  name           = "ValueMetricLog_2"
  pattern        = "ValueError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_processor.function_name}"
  metric_transformation {
    name      = "ValueErrorCount_2"
    namespace = "LogMetric_2"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda-syntax-error-alarm_2" {
  alarm_name                = "lambda2-syntax-error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "SyntaxErrorCount_2"
  namespace                 = "LogMetric_2"
  period                    = 300
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for syntax errors from lambda2"
  alarm_actions             = [aws_sns_topic.error_alerts_2.arn]
  insufficient_data_actions = []
}
resource "aws_cloudwatch_metric_alarm" "lambda-Runtime-Error-alarm_2" {
  alarm_name                = "lambda2-Runtime-Error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "RunTimeErrorCount_2"
  namespace                 = "LogMetric_2"
  period                    = 300 
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for runtime errors from lambda2"
  alarm_actions             = [aws_sns_topic.error_alerts_2.arn]
  insufficient_data_actions = []
}

resource "aws_cloudwatch_metric_alarm" "lambda-value-error-alarm_2" {
  alarm_name                = "lambda2-value-error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "ValueErrorCount_2"
  namespace                 = "LogMetric_2"
  period                    = 300 
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for value errors from lambda2"
  alarm_actions             = [aws_sns_topic.error_alerts_2.arn]
  insufficient_data_actions = []
}

resource "aws_sns_topic" "error_alerts_2" {
  name = "lambda2-error-alerts"
}

resource "aws_sns_topic_subscription" "email_subscription_2" {
  topic_arn = aws_sns_topic.error_alerts_2.arn
  protocol  = "email"
  endpoint  = "detoxdata7@gmail.com"
}

#Lambda 3
resource "aws_cloudwatch_log_metric_filter" "syntax_error_3" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group_3 ]
  name           = "SyntaxMetricLog_3"
  pattern        = "SyntaxError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_uploader.function_name}"
  metric_transformation {
    name      = "SyntaxErrorCount_3"
    namespace = "LogMetric_3"
    value     = "1"
  }
}
resource "aws_cloudwatch_log_metric_filter" "Runtime-Error_3" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group_3 ]
  name           = "RuntimeErrorLog_3"
  pattern        = "RuntimeError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_uploader.function_name}"
  metric_transformation {
    name      = "RunTimeErrorCount_3"
    namespace = "LogMetric_3"
    value     = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "value_error_3" {
  depends_on = [ aws_cloudwatch_log_group.cw_log_group_3 ]
  name           = "ValueMetricLog_3"
  pattern        = "ValueError"
  log_group_name = "/aws/lambda/${aws_lambda_function.s3_uploader.function_name}"
  metric_transformation {
    name      = "ValueErrorCount_3"
    namespace = "LogMetric_3"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda-syntax-error-alarm_3" {
  alarm_name                = "lambda3-syntax-error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "SyntaxErrorCount_3"
  namespace                 = "LogMetric_3"
  period                    = 300
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for syntax errors from lambda3"
  alarm_actions             = [aws_sns_topic.error_alerts_3.arn]
  insufficient_data_actions = []
}
resource "aws_cloudwatch_metric_alarm" "lambda-Runtime-Error-alarm_3" {
  alarm_name                = "lambda3-Runtime-Error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "RunTimeErrorCount_3"
  namespace                 = "LogMetric_3"
  period                    = 300 
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for runtime errors from lambda3"
  alarm_actions             = [aws_sns_topic.error_alerts_3.arn]
  insufficient_data_actions = []
}

resource "aws_cloudwatch_metric_alarm" "lambda-value-error-alarm_3" {
  alarm_name                = "lambda3-value-error-count"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "ValueErrorCount_3"
  namespace                 = "LogMetric_3"
  period                    = 300 
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors logs for value errors from lambda3"
  alarm_actions             = [aws_sns_topic.error_alerts_3.arn]
  insufficient_data_actions = []
}

resource "aws_sns_topic" "error_alerts_3" {
  name = "lambda3-error-alerts"
}

resource "aws_sns_topic_subscription" "email_subscription_3" {
  topic_arn = aws_sns_topic.error_alerts_3.arn
  protocol  = "email"
  endpoint  = "detoxdata7@gmail.com"
}
