import { HostListener, Component, EventEmitter, Input, Output } from '@angular/core';
import { Question } from '../service/question';
declare var $: any;
import * as RecordRTC from 'recordrtc';
import { DomSanitizer } from '@angular/platform-browser';
import { v4 as uuidv4 } from 'uuid';
import * as S3 from 'aws-sdk/clients/s3';
import { GlobalVar } from '../global-variables'
import { AwsLambdaService } from '../service/aws-service.service';

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
        this.childEvent.emit(0);
      }, 5000);
  }
}

public fullResponse!: AWS.Lambda.InvocationResponse;
public lambdaResponse: any;
lambdaName: string = "processRecording";
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
        Bucket: 'bdpaudiobucket',
        Key: objectKey,
        Body: new File([this.blob], "audio.wav"),
    };
    console.log(stringifyObj)
    bucket.upload(params,  (err: any, data: any) => {
        if (err) {
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
  
  //parse the response data from our function
  if(response){
    this.fullResponse = response;
    let res = JSON.parse(response?.Payload?.toString()?? "");
    this.lambdaResponse = res;
    console.log(this.lambdaResponse);
  }
}

}
