const { MongoClient } = require("mongodb");
const MONGODB_URI = process.env.MONGODB_URI;
const DB_NAME = "careride";
const COLLECTION = "demo_requests";
let client;
async function getClient() {
  if (!client) { client = new MongoClient(MONGODB_URI); await client.connect(); }
  return client;
}
exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method Not Allowed" };
  const headers = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" };
  try {
    const { name, email, company, operatorType, fleetSize, message } = JSON.parse(event.body);
    if (!name || !email) return { statusCode: 400, headers, body: JSON.stringify({ error: "Name and email required." }) };
    const db = (await getClient()).db(DB_NAME);
    await db.collection(COLLECTION).insertOne({ name, email, company: company||"", operatorType: operatorType||"", fleetSize: fleetSize||"", message: message||"", submittedAt: new Date(), source: "careride-product-page" });
    return { statusCode: 200, headers, body: JSON.stringify({ success: true }) };
  } catch(err) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: "Server error." }) };
  }
};
