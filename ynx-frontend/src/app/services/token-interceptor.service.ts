import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable, Injector } from '@angular/core';
import { Observable, catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor {

  constructor(private inject: Injector) { }
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    let authService = this.inject.get(AuthService);
    let jwtToken = this.AddTokenHeader(req, authService.getDataFromLS('token'));
    return next.handle(jwtToken).pipe(
      catchError(err => {
        if (err.status === 401) {
          return this.handleRefreshToken(req, next);
        }
        return throwError(err);
      })
    );
  }

  handleRefreshToken(req: HttpRequest<any>, next: HttpHandler) {
    let authService = this.inject.get(AuthService);
    return authService.GenerateRefreshToken().pipe(
      switchMap((data: any) => {
        authService.saveTokens(data);
        return next.handle(this.AddTokenHeader(req, data.access_token))
      }),catchError(err =>{
        authService.logOut();
        return throwError(err);
      })
    );
  }
  AddTokenHeader(req: HttpRequest<any>, token: any) {
    return req.clone({ headers: req.headers.set("Authorization", 'bearer ' + token) });
  }


}
