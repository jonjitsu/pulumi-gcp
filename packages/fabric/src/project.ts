import {
	ComponentResource,
	ResourceOptions,
	mergeOptions,
	output,
	Output,
	Input,
} from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";
const COMPONENT_NAME = "jonjitsu:fabric:project";
const COMPNENT_VERSION = "0.0.1";

interface ProjectArgs {
	name: string;
	prefix?: string;
	createProject?: boolean;
	// in form of "organizations/123456789" or "folders/123456789"
	parent?: string;
	descriptiveName?: string;
	billingAccount?: string;
	autoCreateNetwork?: boolean;
	labels?: { [key: string]: string };
	skipDelete?: boolean;
	services?: string[];
	serviceConfig?: {
		disableOnDestroy: boolean;
		disableDependentServices: boolean;
	};
}

export class Project extends ComponentResource {
	constructor(name: string, args: ProjectArgs, opts?: ResourceOptions) {
		super(COMPONENT_NAME, name, {}, opts);
		opts = mergeOptions(opts, { parent: this });
		const project = createProject(name, args, opts);
	  const services = (args.services || []).map(
	    service => new gcp.projects.Service(`${name}-${service}`, {
	      disableDependentServices: args.serviceConfig?.disableDependentServices || false,
	      disableOnDestroy: args.serviceConfig?.disableOnDestroy || false,
	      service: service,
	      project: project.projectId
	    }, opts)
	  )
	  // new gcp.projects.IAMCustomRole(`${name}-custom-role`, {

	  // }, opts)
	}
}

interface CreateProjectResult {
	projectId: Input<string>;
	number: Input<string>;
	name: Input<string>;
}

function createProject(
	name: string,
	args: ProjectArgs,
	opts?: ResourceOptions,
): CreateProjectResult {
	const projectId = `${args.prefix || ""}${args.name}`;
	if (args.createProject == true || args.createProject == undefined) {
		const projectArgs: gcp.organizations.ProjectArgs = {
			name:
				args.descriptiveName == undefined ? args.name : args.descriptiveName,
			projectId: projectId,
			labels: args.labels,
			skipDelete: args.skipDelete == undefined ? false : args.skipDelete,
			autoCreateNetwork:
				args.autoCreateNetwork == undefined ? false : args.autoCreateNetwork,
		};
		if (args.parent != undefined) {
			if (args.parent.startsWith("organizations/")) {
				projectArgs.orgId = args.parent.slice(14);
			} else if (args.parent.startsWith("folders/")) {
				projectArgs.folderId = args.parent.slice(8);
			}
		}
		if (args.billingAccount != undefined) {
			projectArgs.billingAccount = args.billingAccount;
		}
		return new gcp.organizations.Project(name, projectArgs, opts);
	} else {
		const project = output(
			gcp.organizations.getProject(
				{
					projectId: projectId,
				},
				opts,
			),
		);
    return {
      projectId: project.projectId?.apply((id) => id || projectId) || projectId;
      number: project.number,
      name: project.name
    }
	}
}
