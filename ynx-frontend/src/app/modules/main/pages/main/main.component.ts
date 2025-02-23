import { Component, OnInit, computed, signal } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { PopupMenuComponent } from '../../components/popup-menu/popup-menu.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit{
  collapsed = signal(false);
  sidenavWidth = computed(()=> this.collapsed() ? '65px' : '250px');  
  isHandset: boolean=false;
  constructor(private breakpointObserver:BreakpointObserver,private dialog: MatDialog,){}
  ngOnInit(): void {
    this.breakpointObserver.observe([Breakpoints.Handset, Breakpoints.Small,Breakpoints.XSmall])
    .subscribe(result=>{
      this.isHandset=result.matches;
      console.log(`Is Handset ${this.isHandset}`);
    });
  }

  OpenPopupMenu() {
    var _popup = this.dialog.open(PopupMenuComponent, {
      width: '350px', height: 'auto',
      enterAnimationDuration: '500ms',
      exitAnimationDuration: '500ms',
    });
    _popup.afterClosed().subscribe(item => {});
  }
}
