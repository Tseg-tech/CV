const express = require('express');
const odbc = require('odbc');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;
app.use(express.json()); // to parse JSON body
const connectionString = `Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=C:\\Users\\MSI-\\Documents\\cv\\New folder\\መለማመጃ ጥያቄ.mdb`;
// Add this route to accept score POST


/*async function queryAccessDB() {
  try {
    const connection = await odbc.connect(connectionString);
    const data = await connection.query('SELECT * FROM Exam');
    await connection.close();
    return data;
  } catch (error) {
    console.error('Error querying Access DB:', error);
    throw error;
  }
}
*/

// ✅ Define the function BEFORE using it
async function queryAccess() {
  const connection = await odbc.connect(connectionString);
  const data = await connection.query('SELECT * FROM Exam'); // Replace with your actual table name
  await connection.close();
  return data;
}
/*app.get('/data', async (req, res) => {
  try {
    const rows = await queryAccessDB();
    res.json(rows);
  } catch (error) {
    res.status(500).send('Error fetching data');
  }
});*/

app.get('/data', async (req, res) => {
  try {
    const rows = await queryAccess();

    // Generate HTML table
    let table = '<table border="1" cellpadding="5" cellspacing="0"><tr>';
    const headers = Object.keys(rows[0]);

    // Table headers
    for (const header of headers) {
      table += `<th>${header}</th>`;
    }
    table += '</tr>';

    // Table rows
    for (const row of rows) {
      table += '<tr>';
      for (const header of headers) {
        table += `<td>${row[header]}</td>`;
      }
      table += '</tr>';
    }

    table += '</table>';

    // Send HTML page
    res.send(`
      <html>
        <head>
          <title>Access DB Data</title>
          <style>
            body { font-family: Arial; padding: 20px; }
            table { border-collapse: collapse; }
            th { background: #f0f0f0; }
          </style>
        </head>
        <body>
          <h2>Data from Access Database</h2>
          ${table}
        </body>
      </html>
    `);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error querying database');
  }
});

app.get('/api/questions', async (req, res) => {
  try {
    const rows = await queryAccess();
    res.json(rows);
  } catch (error) {
    console.error('Error fetching questions:', error);
    res.status(500).send('Error fetching questions');
  }
});

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.post('/api/save-result', (req, res) => {
  const { score, total } = req.body;
  const result = {
    score,
    total,
    date: new Date().toISOString(),
  };

 // Save to a file (append results)
  const filePath = path.join(__dirname, 'results.json');

  fs.readFile(filePath, (err, data) => {
    let results = [];
    if (!err) {
      try {
        results = JSON.parse(data);
      } catch {
        results = [];
      }
    }
    results.push(result);
    fs.writeFile(filePath, JSON.stringify(results, null, 2), (err) => {
      if (err) {
        console.error('Error saving result:', err);
        return res.status(500).send('Error saving result');
      }
      res.send('Result saved successfully');
    });
  });
});
// Example query, adjust as per your DB schema & connection code
app.get('/api/questions', isLoggedIn, (req, res) => {
  const questions = db.prepare('SELECT Question_No, Question, Answer1, Answer2, Answer3, Answer4, Correct_Answer FROM Exam').all();
  res.json(questions);
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
