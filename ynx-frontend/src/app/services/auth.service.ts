import { HttpClient, HttpRequest, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, Subject, tap } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private address = environment.API_BASE_URL;
  constructor(private http: HttpClient, private router: Router) { }

  private _refreshrequired = new Subject<void>();
  get Refreshrequired() {
    return this._refreshrequired;
  }

  tokenresp: any;
  private _updatemenu = new Subject<void>();
  get updatemenu() {
    return this._updatemenu;
  }

  handle_post_requests(userObject: any, endpoint: string) {
    console.log(`${userObject}`);
    return this.http.post<any>(`${this.address}/${endpoint}`, userObject)
  }
  handle_get_requests(userObject: any, endpoint: string) {
    return this.http.get<any>(`${this.address}/${endpoint}/${userObject}`)
  }
  handle_get_all_requests(endpoint: string): Observable<any> {
    return this.http.get<any>(`${this.address}/${endpoint}`)
  }

  logOut() {
    localStorage.clear();
    this.router.navigate(['login']);
  }

  GetDatabyToken(token: any) {
    let _token = token.split('.')[1];
    this.tokenresp = JSON.parse(atob(_token));
    return this.tokenresp;
  }

  GenerateRefreshToken() {
    let input = {
      "refresh_token": this.getDataFromLS('refreshtoken'),
      'token_type': 'bearer'
    }
    return this.http.post(this.address + "/auth/refresh-token", input)
  }

  // TOKEN
  saveTokens(res: any) {
    this.saveDataToLS('token',res.access_token);
    this.saveDataToLS('refreshtoken',res.refresh_token);
  }
  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

// SAVE AND GET LOCAL STORAGE(LS)
  saveDataToLS(title: string, value: string) {
    return localStorage.setItem(title, value);
  }
  getDataFromLS(title: string) {
    return localStorage.getItem(title) || "";
  }

  DownloadFile(userObject: any) {
    return this.http.get(`${this.address}/pipe/load-file/${userObject}`, { responseType: 'blob', observe: 'response' });
  }
  Save_and_Add_User(userObject:any,endpoint:string) {
    console.log(userObject);
    return this.http.post<any>(`${this.address}/${endpoint}`, userObject).pipe(
      tap(() => {
        this._refreshrequired.next();
      })
    );
  }
}
