resource "aws_cloudwatch_event_rule" "lambda_trigger_rule" {
  name                = "lambda-every-5-minute"
  description         = "retry scheduled every 5 min"
  schedule_expression = "rate(5 minutes)"
}
resource "aws_cloudwatch_event_target" "lambda_target" {
  arn  = "arn:aws:lambda:eu-west-2:767397911156:function:lambda_handler" #change to lambda1 arn
  rule = aws_cloudwatch_event_rule.lambda_trigger_rule.name
}
resource "aws_lambda_permission" "cloudwatch_lambda_permission" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = "lambda_handler" #change to lambda1 name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_trigger_rule.arn
}
