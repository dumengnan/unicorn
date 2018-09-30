import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/delay';
import 'rxjs/add/operator/do';
import { Observable } from 'rxjs/Observable';

export interface ItemResponse {
    access_token: string,
    token_type: string,
    refresh_token: string,
    expires_in: string,
    scope: string,
    jti: string    
}

export interface currtUserItem {
    aud: Array<string>,
    exp: string,
    user_name:string,
    jti:string,
    client_id:string,
    scope: Array<string>
}

@Injectable()
export class AuthService {

    isLoggedIn = false;

    // store the URL so we can redirect after logging in
    redirectUrl: string;
    loginUrl: string;

    constructor(private http: HttpClient) {}


    login(username: string, password: string): Observable<ItemResponse> {
        this.loginUrl =  "http://192.168.0.6:16003/uaa/oauth/token";
        const headers = new HttpHeaders({'Content-Type' : 'application/x-www-form-urlencoded', 
        'Authorization' : 'Basic YnJvd3Nlcjo='});
        const body = new HttpParams()
            .set('username', username)
            .set('password', password)
            .set('scope', 'ui')
            .set('grant_type', 'password');
        
        return this.http.post<ItemResponse>(this.loginUrl, body, { headers: headers});
    }

    currentUser(token: string): any {
        const checkCurrentUrl = "http://192.168.0.6:16003/uaa/oauth/check_token";
        const headers = new HttpHeaders({'Content-Type' : 'application/x-www-form-urlencoded', 
        'Authorization' : 'Basic YnJvd3Nlcjo='});

        const body = new HttpParams()
        .set('token', token);

        let username;
        this.http.post<currtUserItem>(checkCurrentUrl,body, { headers: headers}).subscribe(
            data => {
                console.log(data.user_name);
                console.log(data.client_id);
            }
        );

        return username;
    }

    logout(): void {
        this.isLoggedIn = false;
    }
}
