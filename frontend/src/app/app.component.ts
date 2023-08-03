import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  HttpClient,
  HttpClientModule,
  HttpHandler,
} from "@angular/common/http";
import { DomSanitizer, SafeResourceUrl } from "@angular/platform-browser";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [CommonModule],
  providers: [HttpClientModule],
  templateUrl: "./app.component.html",
})
export class AppComponent {
  apiUrl = "http://localhost:5000";
  videoUrl!: SafeResourceUrl;

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  startStreaming(): void {
    const startStreamingURL = `${this.apiUrl}/start_streaming`;

    this.http.post<any>(startStreamingURL, {}).subscribe((data) => {
      this.videoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
        `${this.apiUrl}${data.video_url}`
      );
    });
  }
}
