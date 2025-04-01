resource "aws_scheduler_schedule_group" "event_bridge_group" {
  name = local.project_tag
  tags = local.ss_tags
}

resource "aws_scheduler_schedule" "BoxingMondayScheduler" {
  count       = 1
  name        = "${local.project_tag}-Scheduler-Boxing-Class-Monday"
  description = "Scheduler to book my Boxing Class on Monday"
  group_name  = aws_scheduler_schedule_group.event_bridge_group.name

  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression          = "cron(15 07 ? * SUN *)"
  schedule_expression_timezone = "Europe/Lisbon"

  target {
    arn      = module.lambda_function.lambda_function_arn
    role_arn = aws_iam_role.role.arn
    input = jsonencode({
      "users" : [
        "User1", "User2"
      ],
      "className" : "Boxing",
      "classTime" : "07:15"
    })

    retry_policy {
      maximum_event_age_in_seconds = 60
      maximum_retry_attempts       = 0
    }
  }
}
