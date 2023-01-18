import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { QuestionPanelComponent } from './question-panel/question-panel.component';

const routes: Routes = [
  {path: '', component: LoginComponent},
  {path:'home', component:HomeComponent},
  {path:'question', component:QuestionPanelComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
