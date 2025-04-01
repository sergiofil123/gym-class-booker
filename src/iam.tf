/*
  Create IAM Role to be used by schedulers - to allow schedulers to invoke the lambda function
*/

resource "aws_iam_policy" "policy" {
  name        = "${module.lambda_function.lambda_function_name}-eventbridge-schedulers"
  description = "Policy to be used by EventBridge schedulers to allow them to invoke the lambda function"

  policy = jsonencode({
    Version : "2012-10-17"
    Statement : [
      {
        Effect : "Allow",
        Action : [
          "lambda:InvokeFunction"
        ],
        Resource : [
          "arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:${module.lambda_function.lambda_function_name}:*",
          "arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:${module.lambda_function.lambda_function_name}"
        ]
      }
    ]
  })

  tags = local.ss_tags

  depends_on = [module.lambda_function]
}

resource "aws_iam_role" "role" {
  name        = "${module.lambda_function.lambda_function_name}-eventbridge-schedulers"
  description = "Role to be used by EventBridge schedulers to allow them to invoke the lambda function"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect : "Allow",
        Principal : {
          Service : "scheduler.amazonaws.com"
        },
        Action : "sts:AssumeRole",
        Condition : {
          StringEquals : {
            "aws:SourceAccount" : data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })

  tags = local.ss_tags

  depends_on = [aws_iam_policy.policy]
}

resource "aws_iam_role_policy_attachment" "attach-role-policy" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn

  depends_on = [aws_iam_role.role, aws_iam_policy.policy]
}
