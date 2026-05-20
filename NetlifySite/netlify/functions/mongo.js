const { MongoClient } = require('mongodb');
const MONGO_URI = 'mongodb+srv://sentinelUser:SentinelPass123!@cluster0.zfx9ht1.mongodb.net/?appName=Cluster0';
const DB_NAME = 'encounter_db';
let client;
async function getDb() {
  if (!client) { client = new MongoClient(MONGO_URI); await client.connect(); }
  return client.db(DB_NAME);
}
exports.handler = async (event) => {
  const headers = {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Content-Type','Access-Control-Allow-Methods':'POST, OPTIONS','Content-Type':'application/json'};
  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers, body: '' };
  if (event.httpMethod !== 'POST') return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  try {
    const body = JSON.parse(event.body);
    const db = await getDb();
    if (body.action === 'signup') {
      const { first_name, last_name, organization, email, role } = body;
      if (!first_name || !email) return { statusCode: 400, headers, body: JSON.stringify({ error: 'Name and email required' }) };
      const existing = await db.collection('users').findOne({ email: email.toLowerCase() });
      if (existing) return { statusCode: 409, headers, body: JSON.stringify({ error: 'Email already registered' }) };
      await db.collection('users').insertOne({ first_name, last_name, organization, email: email.toLowerCase(), role, created_at: new Date() });
      return { statusCode: 200, headers, body: JSON.stringify({ message: 'Account created successfully!' }) };
    }
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Unknown action' }) };
  } catch (err) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: 'Server error: ' + err.message }) };
  }
};
