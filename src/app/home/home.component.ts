import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {AwsLambdaService} from '../service/aws-service.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  constructor(private _router: Router,private lambdaService: AwsLambdaService){}

  public fullResponse!: AWS.Lambda.InvocationResponse;
  public lambdaResponse: any;
  lambdaName: string = "get_Quizz_test";
  lambdares:boolean=false;

  startQuizz(){
    this._router.navigateByUrl('/quizz');
  }

  callLambda(){
    console.log("calling lambda function")
  }

  public async invokeLambda(){
    let request = {
      x1: 1,
      x2: 2
    };
    //invoke lambda from the lambda service
    let response = await this.lambdaService.invokeLambda(this.lambdaName, request);
    
    //parse the response data from our function
    if(response){
      this.fullResponse = response;
      this.lambdaResponse = JSON.parse(response?.Payload?.toString()?? "");
      console.log(this.lambdaResponse);
      if(this.lambdaResponse.result.y == "3"){
        this.lambdares=true;
      }
    }
    
  }
}
