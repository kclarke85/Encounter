const { MongoClient } = require('mongodb');

const MONGODB_URI = process.env.MONGODB_URI;

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid JSON' }) };
  }

  const client = new MongoClient(MONGODB_URI);

  try {
    await client.connect();
    const db = client.db('encounter_db');

    if (body.action === 'signup') {
      const existing = await db.collection('users').findOne({ email: body.email });
      if (existing) {
        return { statusCode: 409, headers, body: JSON.stringify({ error: 'Email already exists' }) };
      }

      await db.collection('users').insertOne({
        first_name: body.first_name,
        last_name: body.last_name,
        organization: body.organization,
        email: body.email,
        role: body.role,
        created_at: new Date()
      });

      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, message: 'Account created' }) };
    }

    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Unknown action' }) };

  } catch (err) {
    console.error('MongoDB error:', err);
    return { statusCode: 500, headers, body: JSON.stringify({ error: err.message }) };
  } finally {
    await client.close();
  }
};
