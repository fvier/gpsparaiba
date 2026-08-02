mock_provider "coolify" {
  mock_data "coolify_health" {
    defaults = {
      status = "ok"
    }
  }

  mock_data "coolify_version" {
    defaults = {
      version = "4.0.0-test"
    }
  }

}

run "inventory_is_readable" {
  command = plan

  assert {
    condition     = output.coolify.health == "ok"
    error_message = "O inventário não retornou a saúde simulada do Coolify."
  }

  assert {
    condition     = output.coolify.version == "4.0.0-test"
    error_message = "O inventário não retornou a versão simulada do Coolify."
  }
}
