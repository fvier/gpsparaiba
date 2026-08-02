terraform {
  required_version = ">= 1.5.0"

  required_providers {
    hostinger = {
      source  = "hostinger/hostinger"
      version = "~> 0.1.22"
    }
  }
}
