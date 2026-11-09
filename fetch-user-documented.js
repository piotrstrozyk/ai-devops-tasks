
/**
 * Pobiera dane użytkownika z zewnętrznego API.
 *
 * Wysyła żądanie HTTP GET do API, a następnie przetwarza
 * otrzymane dane, zwracając wybrane informacje o użytkowniku.
 *
 * @async
 * @function fetchUserData
 * @param {string|number} userId - Unikalny identyfikator użytkownika.
 * @returns {Promise<Object|null>} Promise zwracający obiekt z danymi użytkownika
 * lub null w przypadku wystąpienia błędu.
 *
 * @returns {Promise<{
*   name: string,
*   email: string,
*   lastLogin: Date
* }|null>}
* Obiekt zawierający imię, adres e-mail i datę ostatniego logowania.
*
* @throws {Error} Błąd HTTP w przypadku nieudanego żądania.
*
* @example
* fetchUserData(123)
*   .then(user => {
*     if (user) {
*       console.log(user.name);
*       console.log(user.email);
*       console.log(user.lastLogin);
*     }
*   });
*/
function fetchUserData(userId) {
 return fetch(`https://api.example.com/users/${userId}`)
   .then(response => {
     if (!response.ok) {
       throw new Error(`HTTP error! status: ${response.status}`);
     }
     return response.json();
   })
   .then(data => {
     return {
       name: data.name,
       email: data.email,
       lastLogin: new Date(data.lastLoginTimestamp)
     };
   })
   .catch(error => {
     console.error('Fetch error:', error);
     return null;
   });
}
