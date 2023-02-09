import { Component, OnInit } from '@angular/core';
import { GlobalVar } from '../global-variables'
import { Router } from '@angular/router';
import { AwsLambdaService } from '../service/aws-service.service';

export interface User {
  username: string;
  password: string;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  username:string;
  password:string;

  constructor(private _router: Router,private lambdaService: AwsLambdaService){
    this.username="";
    this.password="";
  }

public lambdaResponse: any;
lambdares:boolean=false;

public async loginRDS(){
  let lambdaName: string = "lambda-rds-login";
  let request = {
    login: this.username,
    password: this.password,
  };
  //invoke lambda from the lambda service
  let response = await this.lambdaService.invokeLambda(lambdaName, request);
  
  //parse the response data from our function
  if(response){
    let res = JSON.parse(response?.Payload?.toString()?? "");
    this.lambdaResponse = res;
    let data = JSON.parse(this.lambdaResponse.body);
    console.log(data);
    if(data == "Invalid password"){
      console.log('Invalid password')
    }else{
      GlobalVar.connectedUser={id:data[0],username:data[1],password:data[2]};
      console.log("connected with user ",GlobalVar.connectedUser.username," and password ", GlobalVar.connectedUser.password)
      this._router.navigateByUrl('/home')
    }
  }
}


public async registerRDS(){
  let lambdaName: string = "lambda-rds-register";
  let request = {
    login: this.username,
    password: this.password,
  };
  //invoke lambda from the lambda service
  let response = await this.lambdaService.invokeLambda(lambdaName, request);
  
  //parse the response data from our function
  if(response){
    let res = JSON.parse(response?.Payload?.toString()?? "");
    this.lambdaResponse = res;
    let data = JSON.parse(this.lambdaResponse.body);
    console.log(data);
    if(data == "This login already exists"){
      console.log('This login already exists')
    }else{
      GlobalVar.connectedUser={id:data[0],username:data[1],password:data[2]};
      console.log("connected with user ",GlobalVar.connectedUser.username," and password ", GlobalVar.connectedUser.password)
      this._router.navigateByUrl('/home')
    }
  }
}

}