import { HostListener, Component, EventEmitter, Input, Output } from '@angular/core';
import { Question } from '../service/question';
declare var $: any;
import * as RecordRTC from 'recordrtc';
import { DomSanitizer } from '@angular/platform-browser';

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

record:any=null;
  //Will use this flag for toggeling recording
  recording = false;
  //URL of Blob
  url: string="";
  blob:Blob=new Blob();
  error: string="";
  recordVoice:boolean=false;

constructor(private domSanitizer: DomSanitizer){}
  
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

}
