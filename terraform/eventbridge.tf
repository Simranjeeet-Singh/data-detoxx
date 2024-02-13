resource "aws_cloudwatch_event_rule" "lambda_trigger_rule" {
  name                = "lambda-every-5-minutes"
  description         = "retry scheduled every 1 min"
  schedule_expression = "rate(1 minute)"
}
resource "aws_cloudwatch_event_target" "lambda_target" {
  arn  = "arn:aws:lambda:eu-west-2:905418233927:function:example_counter"
  rule = aws_cloudwatch_event_rule.lambda_trigger_rule.name
}
resource "aws_lambda_permission" "cloudwatch_lambda_permission" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = "example_counter"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_trigger_rule.arn
}
