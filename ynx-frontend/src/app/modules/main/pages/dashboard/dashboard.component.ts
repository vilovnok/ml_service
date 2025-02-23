import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AuthService } from 'src/app/services/auth.service';
import { PopupComponent } from '../../components/popup/popup.component';
import { FormBuilder } from '@angular/forms';
import { NgToastService } from 'ng-angular-popup';
import { LoadingHandler } from 'src/app/helpers/loading-handler';
import { PopupDashFilterComponent } from '../../components/popup-dash-filter/popup-dash-filter.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})


export class DashboardComponent implements OnInit {

  public users: any = [];
  colorActivate = false;
  colorRole = false;
  searchtext: any;

  itemsPerPage = 10;
  pages: number[] = [];
  totalPages = 0;
  currentPage = 1;
  display_btn_h: boolean = false;

  loadingHandler = new LoadingHandler();


  constructor(
    private service: AuthService,
    private dialog: MatDialog,
    private fb: FormBuilder,
    private toast: NgToastService) {}

  ngOnInit(): void {this.loadcustomers();}

  sortUsersByRole(users: any) {
    users.forEach((user: any) => {
    user.created_at = new Date(user.created_at).toString().split('GMT')[0].trim();});
    users.sort((a:any, b:any) => {
      if (a.role === 'admin' && b.role !== 'admin') {
        return -1;
      } else if (a.role !== 'admin' && b.role === 'admin') {
        return 1; 
      } else {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      }
    });
  }

  loadcustomers() {
    this.loadingHandler.showLoading();
    this.service.handle_get_all_requests('user/profiles').subscribe(result => {
      let totalItems = result.posts.length;
      if (totalItems > 0) {
        this.display_btn_h = true;
        this.users = result.posts;
        this.loadingHandler.hidenLoading()
        this.Paginator(totalItems);
        this.sortUsersByRole(this.users);
      } else {
        this.loadingHandler.hidenLoading();
      }
    });
  }

  editcustomer(user_id: any) {
    this.OpenpopupEditUser(user_id, 'Edit Customer');
  }

  removecustomer(user_id: number) {
    this.RemoveUser(user_id);
  }

  addcustomer() {
    this.OpenpopupEditUser(-1, 'Add Customer');
  }

  OpenPopupDashFilter(task_id: any, file_name: any) {
    const mediaQueryList1200 = window.matchMedia('(min-width: 1200px)');
    const mediaQueryList992=window.matchMedia('(min-width: 992px)')
    const mediaQueryList768 = window.matchMedia('(min-width: 768px) and (max-width: 991px)');
    const mediaQueryList480 = window.matchMedia('(max-width: 767px)');
    
    let dialogWidth: string;
    if (mediaQueryList1200.matches) {
      dialogWidth = '30%';
    } else if (mediaQueryList992.matches) {
      dialogWidth = '40%';
    } else if (mediaQueryList768.matches) {
      dialogWidth = '50%';
    } else if (mediaQueryList480.matches) {
      dialogWidth = '80%';
    } else {
      dialogWidth = '90%';
    }

    const updateDialogSize = () => {
      if (mediaQueryList1200.matches) {
        dialogWidth = '30%';
      } else if (mediaQueryList992.matches) {
        dialogWidth = '40%';
      } else if (mediaQueryList768.matches) {
        dialogWidth = '50%';
      } else if (mediaQueryList480.matches) {
        dialogWidth = '80%';
      } else {
        dialogWidth = '90%';
      }
      dialogRef.updateSize(dialogWidth, 'auto');
    };

    mediaQueryList1200.addEventListener('change', updateDialogSize);
    mediaQueryList992.addEventListener('change', updateDialogSize);
    mediaQueryList768.addEventListener('change', updateDialogSize);
    mediaQueryList480.addEventListener('change', updateDialogSize);
    var dialogRef = this.dialog.open(PopupDashFilterComponent, {
      width: dialogWidth, 
      height: 'auto',
      enterAnimationDuration: '500ms',
      exitAnimationDuration: '500ms',
    });
    dialogRef.afterClosed().subscribe(item => {
      // this.loadcustomer();
    });
  }

  OpenpopupEditUser(user_id: any, title: any) {
    var _popup = this.dialog.open(PopupComponent, {
      width: '40%', height: '40%',
      enterAnimationDuration: '500ms',
      exitAnimationDuration: '500ms',
      data: { title: title, user_id: user_id }

    });
    _popup.afterClosed().subscribe(item => {
      this.loadcustomers();
    });
  }

  RemoveUser(user_id: number) {
    if (confirm('Вы хотите удалить пользователя?')) {
      const req_form = this.fb.group({ user_id: user_id }).value;
      this.service.handle_post_requests(req_form, 'user/remove').subscribe(res => {
        this.loadcustomers();
        this.toast.success({ detail: 'success', summary: 'Пользователь удален!' });
      });
    }
  }

  ////// Paginator
  Paginator(totalItems: number) {
    if (totalItems) {
      this.totalPages = Math.ceil(totalItems / this.itemsPerPage);
      console.log(this.totalPages);
      this.pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
    }
  }

  pageClicked(page: number) {
    if (page > this.totalPages) return;
    if (page < 1) return;
    this.currentPage = page;
  }

  get paginatedData() {
    const start = (this.currentPage - 1) * (this.itemsPerPage);
    const end = (start + this.itemsPerPage)
    return this.users.slice(start, end);
  }

  clearSearch() {
    this.searchtext = '';
  }

  navigateToFirstPage() {
    this.currentPage = 1;
  }

  navigateBackward() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  navigateForward() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  navigateToLastPage() {
    this.currentPage = this.totalPages;
  }

  add_filter() {
    // this.OpenpopupFilter(12, 'test.txt');
  }
}
