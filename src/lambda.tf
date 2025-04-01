data "archive_file" "python_code" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_code/src"
  output_path = "${path.module}/lambda_code/target/lambda_code.zip"
}

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  # variable to control if a new version should be published
  publish = false

  function_name = local.project_tag
  description   = "Book my Gym Classes"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.13"
  architectures = ["x86_64"]
  timeout       = 60

  create_package         = false
  local_existing_package = "${path.module}/lambda_code/target/lambda_code.zip"

  // Attach existing AWS policy for Lambda VPC
  attach_policies    = true
  number_of_policies = 1
  policies = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
  ]

  // Cloudwatch Log Group
  cloudwatch_logs_retention_in_days = 30

  environment_variables = {
    GYM_URL_API         = var.config_gym_url_api
    USER_CONFIGS        = var.config_user
    GYM_CLASSES_CONFIGS = var.config_gym_classes
  }

  tags = local.ss_tags
}


