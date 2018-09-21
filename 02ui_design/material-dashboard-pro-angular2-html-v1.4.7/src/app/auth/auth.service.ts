import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/delay';

@Injectable()
export class AuthService {

    isLoggedIn = false;

    // store the URL so we can redirect after logging in
    redirectUrl: string;

    constructor(private http: HttpClient) {}


    login(username: string, password: string): Observable<boolean> {
        const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });
        const body = new HttpParams()
            .set('email', username)
            .set('password', password);

        console.log("The username is  %s ", username);
        return this.http.post<boolean>('/dmp-probe-site/loginuser/doLogin.action', body, { headers: headers});
        // return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
    }

    logout(): void {
        this.isLoggedIn = false;
    }
}
