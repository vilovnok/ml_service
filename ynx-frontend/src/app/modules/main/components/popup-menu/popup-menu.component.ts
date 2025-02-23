import { Component, OnInit, signal } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';

export type MenuItem = {
  label: string,
  route?: string
}

@Component({
  selector: 'app-popup-menu',
  templateUrl: './popup-menu.component.html',
  styleUrls: ['./popup-menu.component.scss']
})
export class PopupMenuComponent {
  
  closemessage = 'Closed';
  constructor(
    private ref: MatDialogRef<PopupMenuComponent>,
    private router: Router,private route: ActivatedRoute) { }

  closepopup() {this.ref.close(this.closemessage);}
  menuItems = signal<MenuItem[]>([
    { label: 'search', route: 'home/search' },
    { label: 'pipeline', route: 'home/pipeline' },
    { label: 'dashboard', route: 'home/dashboard' }
  ]);
  getToPage(route:any){
    this.router.navigate([`/${route}`])
    this.closepopup();
  }
}
