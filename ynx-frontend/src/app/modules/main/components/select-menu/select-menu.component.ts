import { Component } from '@angular/core';

@Component({
  selector: 'app-select-menu',
  templateUrl: './select-menu.component.html',
  styleUrls: ['./select-menu.component.scss']
})
export class SelectMenuComponent {

date:string='22.02.22';
dates: any[]=['html','css','rust','python','lplp'];
isVisibleFlag:boolean=false;

toggleVisibility(){
this.isVisibleFlag=!this.isVisibleFlag;
}

choiceDate(){
  console.log('Roate');
}
// visibilty(){
//   this.visib=!this.visib;
//   console.log('ПОказать или закрыть !!!');
// }
isVisible(){
return this.isVisibleFlag;
}

selectDate(date:string) {
  this.date=date;

}

  
}
