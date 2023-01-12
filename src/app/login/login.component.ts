import { Component, OnInit } from '@angular/core';
import { v4 as uuidv4 } from 'uuid';
import * as AWS from 'aws-sdk/global';
import * as S3 from 'aws-sdk/clients/s3';

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
  connectedUser:User;
  credentialMatch:boolean;
  loginFinished:boolean;
  userList:User[]|undefined=[];

  constructor(){
    this.username="";
    this.password="";
    this.connectedUser={username:"",password:""};
    this.credentialMatch=false;
    this.loginFinished=false;
    this.loadLogin();
  }



  OnInit(){
    
  }

  async loadLogin(){
    console.log('listing login bucket ...');
    const bucket = new S3(
      {
        accessKeyId: 'ASIAUGNLVVIW53DTHVF3',
        secretAccessKey: 'TeZqiQvA7FlgPCvy6ZUvxrDfgCdHse1mro3H6Wgk',
        sessionToken:'FwoGZXIvYXdzEHEaDJN4CrAtXav8SoQ2viK9AW16h1r+kvHzeqp8ZiR38XgraNNwNDMtM+8KoJ1C/FbzBPa9d12AGrz8mGnc1N3rzO4xalg/ISx1Bl94rt3jWRQTISG3yVcgP03XnPX0rwijGf02tYIVy2uF3DgWi2rBa2Lfjiz1SCZ3h8ybtkeeg3u0FukDJH6UqVhRFEr0x5usyCTecBVd6FfH2Sh4mkvHI/wVIhnKpcg0z3+r2DQpSD1+MzDFPmeabg4mb+flO61prezWXpgA+NfmVFPwMiii6/6dBjItaoh7Ew2kb2ppRArRJFEjksyPbCMrolL/B4okla3aOKhaNaehg2CxOo+7DhIs',
        region: 'us-east-1'
      }
      );
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

  register(){
    if(this.username!="" && this.password!=""){
      console.log("register with account ", this.username)
      const object:User={username:this.username, password:this.password};
      const stringifyObj = JSON.stringify(object);
      const bucket = new S3(
        {
          accessKeyId: 'ASIAUGNLVVIW53DTHVF3',
          secretAccessKey: 'TeZqiQvA7FlgPCvy6ZUvxrDfgCdHse1mro3H6Wgk',
          sessionToken:'FwoGZXIvYXdzEHEaDJN4CrAtXav8SoQ2viK9AW16h1r+kvHzeqp8ZiR38XgraNNwNDMtM+8KoJ1C/FbzBPa9d12AGrz8mGnc1N3rzO4xalg/ISx1Bl94rt3jWRQTISG3yVcgP03XnPX0rwijGf02tYIVy2uF3DgWi2rBa2Lfjiz1SCZ3h8ybtkeeg3u0FukDJH6UqVhRFEr0x5usyCTecBVd6FfH2Sh4mkvHI/wVIhnKpcg0z3+r2DQpSD1+MzDFPmeabg4mb+flO61prezWXpgA+NfmVFPwMiii6/6dBjItaoh7Ew2kb2ppRArRJFEjksyPbCMrolL/B4okla3aOKhaNaehg2CxOo+7DhIs',
          region: 'us-east-1'
        }
        );
        const params = {
            Bucket: 'bdploginbucket',
            Key: uuidv4(),
            Body: stringifyObj
        };
        console.log(stringifyObj)
        bucket.upload(params, function (err: any, data: any) {
            if (err) {
                console.log('There was an error uploading your file: ', err);
                return false;
            }
            console.log('Successfully uploaded file.', data);
            return true;
        });

    }else{
      alert("error");
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
          this.connectedUser={username:this.username,password:this.password};
          const message = "connected with user " + this.connectedUser.username;
          console.log("connected with user ",this.connectedUser.username," and password ", this.connectedUser.password)
          this.credentialMatch=false;
          alert(message);
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