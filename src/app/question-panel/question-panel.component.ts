import { HostListener, Component, EventEmitter, Input, Output } from '@angular/core';
import { Question } from '../service/question';
declare var $: any;
import * as RecordRTC from 'recordrtc';
import { DomSanitizer } from '@angular/platform-browser';
import { v4 as uuidv4 } from 'uuid';
import * as S3 from 'aws-sdk/clients/s3';
import { GlobalVar } from '../global-variables'
import { AwsLambdaService } from '../service/aws-service.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-question-panel',
  templateUrl: './question-panel.component.html',
  styleUrls: ['./question-panel.component.css']
})
export class QuestionPanelComponent  {
  @Input()
  question!: Question;

  @Output() childEvent = new EventEmitter();
returnAnswer(index:number){
  if(!this.recordVoice){
    const Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
    });
    let i= index+1;
    let message = 'Vous avez choisi la réponse ' + i;
    Toast.fire({
      icon: 'success',
      title: message,
    });

    this.childEvent.emit(index);
  } 
}

@HostListener('document:keyup', ['$event'])
async handleKeyboardEvent(event: KeyboardEvent) {
  if (event.key == ' ' && !this.recordVoice ) {
    this.recordVoice=true;
    this.initiateRecording();
    console.log('enter pressed')
    setTimeout(()=>{
        this.recordVoice = false;
        this.stopRecording();
        this.uploadRecordToS3(); 
      }, 5000);
  }
}

public fullResponse!: AWS.Lambda.InvocationResponse;
public lambdaResponse: any;
lambdaName: string = "lambda-test-model";
lambdares:boolean=false;

record:any=null;
  //Will use this flag for toggeling recording
  recording = false;
  //URL of Blob
  url: string="";
  blob:Blob=new Blob();
  error: string="";
  recordVoice:boolean=false;

constructor(private domSanitizer: DomSanitizer, private lambdaService: AwsLambdaService){}
  
sanitize(url: string) {
  return this.domSanitizer.bypassSecurityTrustUrl(url);
}

initiateRecording() {

  this.recording = true;
  let mediaConstraints = {
    video: false,
    audio: true
  };
  navigator.mediaDevices
    .getUserMedia(mediaConstraints)
    .then(this.successCallback.bind(this), this.errorCallback.bind(this));
}

successCallback(stream: any) {
  let type = "audio/wav" as const;
  let nbChannels = 1 as const;
  let rate = 48000 as const;
  var options = {
    mimeType: type,
    numberOfAudioChannels: nbChannels,
    sampleRate: rate,
  };
  //Start Actuall Recording
  var StereoAudioRecorder = RecordRTC.StereoAudioRecorder;
  this.record = new StereoAudioRecorder(stream, options);
  this.record.record();
}

stopRecording() {
  this.recording = false;
  this.record.stop(this.processRecording.bind(this));
}

processRecording(blob: Blob | MediaSource) {
  this.url = URL.createObjectURL(blob);
  this.blob=blob as Blob;
  console.log("blob", blob);
  console.log("url", this.url);
}

errorCallback(error: any) {
  this.error = 'Can not play audio in your browser';
}


download(url:string){
  let a = document.createElement('a');
  document.body.appendChild(a);
  a.setAttribute('style', 'display: none');
  a.href = url;
  a.download = "blob.wav";
  a.click();
  window.URL.revokeObjectURL(url);
  a.remove();
}


public async uploadRecordToS3(){
  const object={blob: this.blob};
  const stringifyObj = JSON.stringify(object);
  console.log(stringifyObj)
  const bucket = new S3(GlobalVar.credentials);
  const objectKey = uuidv4();
    const params = {
        Bucket: 'big-data-audio-file',
        Key: objectKey,
        Body: new File([this.blob], "audio.wav"),
    };
    console.log(stringifyObj)
    bucket.upload(params,  (err: any, data: any) => {
        if (err) {
          const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
              toast.addEventListener('mouseenter', Swal.stopTimer)
              toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
          });
          Toast.fire({
            icon: 'error',
            title: "Erreur serveur (bucket)"
          });
            console.log('There was an error uploading your file: ', err);
            return null;
        }
        console.log('Successfully uploaded file.', data);
        this.ProcessRecord(data.key);
        console.log('key:', data.key)
        return objectKey;
    });
}

public async ProcessRecord(recordKey:number){
  let request = {
    key: recordKey
  };
  //invoke lambda from the lambda service
  console.log('calling lambda to process the recording ...')
  let response = await this.lambdaService.invokeLambda(this.lambdaName, request);

  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  });
  
  //parse the response data from our function
  if(response){
    this.fullResponse = response;
    let res = JSON.parse(response?.Payload?.toString()?? "");
    this.lambdaResponse = res;
    let data = JSON.parse(this.lambdaResponse.body);
    console.log(data);
    const Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
    });
    if(data == "Could not indentify response"){
      console.log('Could not indentify response')
      Toast.fire({
        icon: 'error',
        title: "Nous n'avons pas compris votre réponse"
      });
    }else{
      if(data = "un"){
        Toast.fire({
          icon: 'success',
          title: 'Vous avez choisi la réponse 1'
        });
        this.childEvent.emit(0);
      }else if(data =="deux"){
        Toast.fire({
          icon: 'success',
          title: 'Vous avez choisi la réponse 2'
        });
        this.childEvent.emit(1)
      }else if(data =="trois"){
        Toast.fire({
          icon: 'success',
          title: 'Vous avez choisi la réponse 3'
        });
        this.childEvent.emit(2)
      }else if(data =="quatre"){
        Toast.fire({
          icon: 'success',
          title: 'Vous avez choisi la réponse 4'
        });
        this.childEvent.emit(3)
      }else{
        Toast.fire({
          icon: 'error',
          title: "Nous n'avons pas compris votre réponse"
        });
      }
      
    }
  }else{
    Toast.fire({
      icon: 'error',
      title: "Erreur serveur (model)"
    });
  }
}

}
