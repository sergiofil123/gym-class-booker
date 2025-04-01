locals {
  project_tag = "Gym-Class-Booker"
  ss_tags = {
    "ss:project"   = local.project_tag
    "ss:managedBy" = "Tofu"
  }
}

variable "config_gym_url_api" {
  type        = string
  default     = "https://gym.com/api/"
  description = "URL for Gym REST API"
}

variable "config_gym_classes" {
  type        = string
  default     = <<EOF
[{"name": "ABS", "id": 16001},{"name": "Boxing", "id": 17810},{"name": "Run", "id": 21634},{"name": "Cycling", "id": 16203}]
EOF
  description = "List of classes that I want to book"
}

variable "config_user" {
  type        = string
  default     = <<EOF
[{"name": "User1","user_id": 100,"user_center_id": 21,"email": "user1@email.com","password": "123"},
{"name": "User2","user_id": 101,"user_center_id": 23,"email": "user2@email.com","password": "123"}]
EOF
  description = "List with users"
}
