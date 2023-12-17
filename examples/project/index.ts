import * as pulumi from "@pulumi/pulumi";
import { Project } from "@jonjitsu/fabric";


export const project = new Project("my-project");

