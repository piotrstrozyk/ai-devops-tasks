
import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException


class JenkinsManager:
    def __init__(self, url, username, api_token):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, api_token)
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        self.timeout = 15

    def _request(self, method, endpoint, **kwargs):
        """Wspólna obsługa zapytań HTTP."""
        url = f"{self.url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )

            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "?"
            print(f"[HTTP ERROR] Status {status}: {e}")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Nie można połączyć się z Jenkins.")
        except requests.exceptions.Timeout:
            print("[ERROR] Przekroczono czas oczekiwania.")
        except RequestException as e:
            print(f"[ERROR] Błąd zapytania: {e}")

        return None

    def list_jobs(self):
        """Pobiera listę wszystkich zadań."""
        response = self._request(
            "GET",
            "/api/json?tree=jobs[name,url,color]"
        )

        if not response:
            return []

        try:
            jobs = response.json().get("jobs", [])

            print("\n=== LISTA ZADAŃ ===")

            for job in jobs:
                print(
                    f"Nazwa: {job['name']} | "
                    f"Status: {job.get('color', 'UNKNOWN')} | "
                    f"URL: {job['url']}"
                )

            return jobs

        except ValueError:
            print("[ERROR] Nieprawidłowa odpowiedź JSON.")
            return []

    def get_last_build_status(self, job_name):
        """Sprawdza status ostatniego buildu."""
        endpoint = (
            f"/job/{job_name}/lastBuild/api/json"
            "?tree=number,result,building,timestamp,url"
        )

        response = self._request("GET", endpoint)

        if not response:
            return None

        try:
            build = response.json()

            status = (
                "BUILDING"
                if build.get("building")
                else build.get("result", "UNKNOWN")
            )

            print(f"\n=== STATUS: {job_name} ===")
            print(f"Build number: {build.get('number')}")
            print(f"Status: {status}")
            print(f"URL: {build.get('url')}")

            return build

        except ValueError:
            print("[ERROR] Nieprawidłowa odpowiedź JSON.")
            return None

    def trigger_job(self, job_name):
        """Uruchamia wybrane zadanie."""
        endpoint = f"/job/{job_name}/build"

        response = self._request("POST", endpoint)

        if response:
            queue_url = response.headers.get("Location")

            print(f"[SUCCESS] Zadanie '{job_name}' zostało uruchomione.")

            if queue_url:
                print(f"Queue URL: {queue_url}")

            return True

        return False

    def close(self):
        self.session.close()


def main():
    # Konfiguracja przez zmienne środowiskowe
    jenkins_url = os.getenv("JENKINS_URL")
    username = os.getenv("JENKINS_USER")
    api_token = os.getenv("JENKINS_TOKEN")

    if not all([jenkins_url, username, api_token]):
        print("[ERROR] Ustaw zmienne środowiskowe:")
        print("JENKINS_URL, JENKINS_USER, JENKINS_TOKEN")
        sys.exit(1)

    jenkins = JenkinsManager(
        jenkins_url,
        username,
        api_token
    )

    try:
        while True:
            print("\n===== JENKINS MANAGER =====")
            print("1. Lista wszystkich zadań")
            print("2. Status ostatniego buildu")
            print("3. Uruchom zadanie")
            print("4. Wyjście")

            choice = input("\nWybierz opcję: ").strip()

            if choice == "1":
                jenkins.list_jobs()

            elif choice == "2":
                job_name = input("Nazwa zadania: ").strip()

                if job_name:
                    jenkins.get_last_build_status(job_name)

            elif choice == "3":
                job_name = input("Nazwa zadania: ").strip()

                if job_name:
                    jenkins.trigger_job(job_name)

            elif choice == "4":
                print("Zamykanie programu...")
                break

            else:
                print("[ERROR] Nieprawidłowa opcja.")

    finally:
        jenkins.close()


if __name__ == "__main__":
    main()
