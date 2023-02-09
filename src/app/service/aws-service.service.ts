import { Injectable } from '@angular/core';
import * as AWS from 'aws-sdk';
import { Lambda } from 'aws-sdk';
import { GlobalVar } from '../global-variables'

@Injectable({
  providedIn: 'root'
})
export class AwsLambdaService {

  private lambdaService: AWS.Lambda = new AWS.Lambda(GlobalVar.credentials);

  constructor() {}

  private async runSetup() {
    if (this.lambdaService) {
        return this.lambdaService;
    } else {
        let config: AWS.STS.ClientConfiguration = GlobalVar.credentials;
        console.log(config);
        console.log('CREATING LAMBDA SERVICE!');
        this.lambdaService = new AWS.Lambda(config);
        return this.lambdaService;
    }
  }

  public async invokeLambda(functionName: string, functionArgs: any) : 
   Promise<AWS.Lambda.InvocationResponse> {
    await this.runSetup();
    let request: AWS.Lambda.InvocationRequest = {
      FunctionName: functionName,
      Payload: JSON.stringify(functionArgs),
      InvocationType: 'RequestResponse'
    };
    return new Promise(async (resolve, reject)=>{
      await this.lambdaService.invoke(request,  (err, data) => {
        if(err){
          reject(err);
          return;
        }
        resolve(data);
      });
    });
}
}
