data "coolify_health" "current" {}
data "coolify_version" "current" {}
data "coolify_servers" "all" {}
data "coolify_projects" "all" {}
data "coolify_applications" "all" {}
data "coolify_deployments" "all" {}

output "coolify" {
  value = {
    health  = data.coolify_health.current.status
    version = data.coolify_version.current.version
  }
}

output "servers" {
  value = [for server in data.coolify_servers.all.servers : {
    uuid         = server.uuid
    name         = server.name
    ip           = server.ip
    reachable    = server.is_reachable
    usable       = server.is_usable
    build_server = server.is_build_server
  }]
}

output "projects" {
  value = [for project in data.coolify_projects.all.projects : {
    uuid = project.uuid
    name = project.name
  }]
}

output "applications" {
  value = [for application in data.coolify_applications.all.applications : {
    uuid       = application.uuid
    name       = application.name
    status     = application.status
    domains    = application.domains
    repository = application.git_repository
    branch     = application.git_branch
    build_pack = application.build_pack
  }]
}

output "deployments" {
  value = [for deployment in data.coolify_deployments.all.deployments : {
    uuid        = deployment.uuid
    server_uuid = deployment.server_uuid
    status      = deployment.status
  }]
}
