import { Component, Input, OnInit, computed, signal } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

export type MenuItem = {
  icon: string,
  label: string,
  route?: string
}

@Component({
  selector: 'app-custom-sidenav',
  templateUrl: './custom-sidenav.component.html',
  styleUrls: ['./custom-sidenav.component.scss']
})
export class CustomSidenavComponent implements OnInit {

  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    this.auth.updatemenu.subscribe(res => {
      this.menuDisplay();});
    this.menuDisplay();
    this.get_balance();
  }


  displayDashboard = false;

  currentRole: any;
  currentActive: any;
  currentFirstName: any;
  currentLastName: any;
  currentUser_id: any;
  currentBalance: any;

  sideNavCollapsed = signal(false);
  @Input() set collapsed(val: boolean) {
    this.sideNavCollapsed.set(val);
  }

  menuItems = signal<MenuItem[]>([
    { icon: 'bolt', label: 'generate', route: 'generate' },
    { icon: 'auto_awesome', label: 'illustrate', route: 'illustrate' },
    { icon: 'dashboard', label: 'dashboard', route: 'dashboard' }
  ]);


  picSize = computed(() => this.sideNavCollapsed() ? '32' : '100');

  menuDisplay() {
    if (this.auth.getDataFromLS('token') != '') {
      this.currentFirstName = this.auth.GetDatabyToken(this.auth.getDataFromLS('token')).first_name;
      this.currentLastName = this.auth.GetDatabyToken(this.auth.getDataFromLS('token')).last_name;
      this.currentUser_id = this.auth.GetDatabyToken(this.auth.getDataFromLS('token')).id;
      this.GetDataVerify(this.currentUser_id);
    }
  }

  GetDataVerify(user_id: any) {
    this.auth.handle_get_requests(user_id,'verify/verify-user').subscribe(result => {
      this.currentRole = result.role;
      this.currentActive = result.active;
      console.log("Custome Active and Role: ", this.currentActive, this.currentRole);
      this.auth.saveDataToLS('role',this.currentRole);
      this.displayDashboard = this.currentRole == "user";
      if (this.displayDashboard) {
        const currentMenuItems = this.menuItems();
        currentMenuItems.splice(2, 1);
        this.menuItems.set(currentMenuItems);
      }
    });
  }


  get_balance(){
    this.auth.handle_get_requests('','generate/get_balance').subscribe(result => {
      this.currentBalance = result['balance'];
      console.log(this.currentBalance);
    })
  }
  logOut(): void {
    this.auth.logOut();
  }
}
