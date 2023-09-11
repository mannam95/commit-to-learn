
devtfinit:
	@terraform init -reconfigure -var-file=config/dev.auto.tfvars -backend-config=config/dev.backend.hcl

devtfvalidate:
	@terraform validate

devtfplan:
	@terraform plan -var-file=config/dev.auto.tfvars

devtfapply:
	@terraform apply -var-file=config/dev.auto.tfvars

devtfdestroy:
	@terraform destroy -var-file=config/dev.auto.tfvars


prodtfinit:
	@terraform init -reconfigure -var-file=config/prod.auto.tfvars -backend-config=config/prod.backend.hcl

prodtfvalidate:
	@terraform validate

prodtfplan:
	@terraform plan -var-file=config/prod.auto.tfvars

prodtfapply:
	@terraform apply -var-file=config/prod.auto.tfvars

prodtfdestroy:
	@terraform destroy -var-file=config/prod.auto.tfvars