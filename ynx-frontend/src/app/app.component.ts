import { Component, computed, signal } from '@angular/core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'event-index';

  // collapsed = signal(false);
  // sidenavWidth = computed(()=> this.collapsed() ? '65px' : '250px'); 
  
  
}
