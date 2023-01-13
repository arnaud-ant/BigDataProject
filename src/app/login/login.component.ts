import { Component, OnInit } from '@angular/core';
import { v4 as uuidv4 } from 'uuid';
import * as AWS from 'aws-sdk/global';
import * as S3 from 'aws-sdk/clients/s3';
import { GlobalVar } from '../global-variables'
import { Router } from '@angular/router';

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
  credentialMatch:boolean;
  userList:User[]|undefined=[];

  constructor(private _router: Router){
    this.username="";
    this.password="";
    this.credentialMatch=false;
    this.loadLogin();
  }



  OnInit(){
    
  }

  async loadLogin(){
    console.log('listing login bucket ...');
    const bucket = new S3(GlobalVar.credentials);
      const params = {
          Bucket: 'bdploginbucket'
      };
      

       const loginres= await bucket.listObjects(params, async (err, data) => {
          if (err) {
            console.log('There was an error listing the bucket: ', err);
            return false;
          }else{
            const objectList = data.Contents;
            for(const obj of objectList??[]){
              const params = {
                Bucket: 'bdploginbucket',
                Key: obj.Key|| ''
              };
              const res = await bucket.getObject(params, (err, data) => {
                if (err) {
                  console.log(err);
                } else {
                  try {
                    
                    const loginobject = JSON.parse(data?.Body?.toString()?? "");
                    this.userList?.push(loginobject);
                    console.log(loginobject);
                    
                  } catch (e) {
                    console.log(e);
                  }
                }
              });
              const promiseRes=await Promise.all([bucket.getObject()]);
              console.log('result of the promise ',promiseRes)
            };
            return true;
          }
        });
        const loginRes=await Promise.all([bucket.listObjects()]);
  }

  onSubmit(){
    if (this.username=="test" && this.password=="test")
    {
      alert("Connecté");
    }
  }

  checkExistingUser(){
    let userAlreadyExist=false;
    this.userList?.forEach(user =>{
      if(this.username == user.username){
        userAlreadyExist=true;
      }
    });
    return userAlreadyExist;
  }

  register(){
    if(!this.checkExistingUser()){
      if(this.username!="" && this.password!=""){
        console.log("register with account ", this.username)
        const object:User={username:this.username, password:this.password};
        const stringifyObj = JSON.stringify(object);
        const bucket = new S3(GlobalVar.credentials);
          const params = {
              Bucket: 'bdploginbucket',
              Key: uuidv4(),
              Body: stringifyObj
          };
          console.log(stringifyObj)
          bucket.upload(params,  (err: any, data: any) => {
              if (err) {
                  console.log('There was an error uploading your file: ', err);
                  return false;
              }
              console.log('Successfully uploaded file.', data);
              GlobalVar.connectedUser={username:this.username,password:this.password};
              console.log("connected with user ",GlobalVar.connectedUser.username," and password ", GlobalVar.connectedUser.password)
              this._router.navigateByUrl('/home')
              return true;
          });
  
      }else{
        alert("error");
      }
    }else{
      alert('this user already exists')
    }
  }

  async login(){
    if(this.username!="" && this.password!=""){
      console.log("trying login with account ", this.username)
      
      this.userList?.forEach(user => {
        if(!this.credentialMatch && user.username == this.username && user.password == this.password){
          this.credentialMatch=true;
        }
      });

        if(this.credentialMatch ){
          GlobalVar.connectedUser={username:this.username,password:this.password};
          const message = "connected with user " + GlobalVar.connectedUser.username;
          console.log("connected with user ",GlobalVar.connectedUser.username," and password ", GlobalVar.connectedUser.password)
          this.credentialMatch=false;
          this._router.navigateByUrl('/home')
        }else{
          console.log(this.userList)
          alert("there is no user with this password");
          console.log("no match with user ",this.username," and password ", this.password);
        }
        

    }else{
      alert("error, please enter valid credentials");
    }
  }
}