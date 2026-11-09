Możesz wykorzystać metodę `filter()`, następnie `sort()` i na końcu `map()`:

javascript

```javascript
function getCompletedTaskTitles(tasks) {
  return tasks
    .filter(task => task.status === "completed")
    .sort((a, b) => a.id - b.id)
    .map(task => task.title);
}
```

### Przykład użycia

javascript

```javascript
const tasks = [
  { id: 3, title: "Nauczyć się Reacta", status: "completed" },
  { id: 1, title: "Poznać JavaScript", status: "completed" },
  { id: 2, title: "Zrobić projekt", status: "pending" },
  { id: 4, title: "Nauczyć się Node.js", status: "completed" }
];

console.log(getCompletedTaskTitles(tasks));
```

Wynik:

javascript

```javascript
[
  "Poznać JavaScript",
  "Nauczyć się Reacta",
  "Nauczyć się Node.js"
]
```

### Jak to działa?

1. `filter()` – wybiera tylko zadania ze statusem `"completed"`.
2. `sort()` – sortuje zadania rosnąco według `id`.
3. `map()` – tworzy nową tablicę zawierającą wyłącznie tytuły (`title`).

Ważne: `sort()` modyfikuje oryginalną tablicę wynikową z `filter()`, ale nie zmienia tablicy `tasks`, ponieważ `filter()` tworzy nową tablicę.