// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

// Setup type definitions for built-in Supabase Runtime APIs
import "https://esm.sh/v135/@supabase/functions-js@2.4.1/src/edge-runtime.d.ts";

import { createClient } from "npm:@supabase/supabase-js@2.42.0";
import { Database } from "../_shared/database.types.ts";

import { Pinecone } from "https://esm.sh/@pinecone-database/pinecone";

const supabase = createClient<Database>(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

const model = new Supabase.ai.Session("gte-small");

const pinecone_api_key = Deno.env.get("PINECONE_API_KEY") ?? "";
const pinecone_index_name = Deno.env.get("PINECONE_INDEX_NAME") ?? "";
const pinecone_namespace = Deno.env.get("PINECONE_NAMESPACE") ?? "";

const pc = new Pinecone({ apiKey: pinecone_api_key });
const index = pc.index(pinecone_index_name);

const filter = {};
const topK = 3;

Deno.serve(async (req) => {
  const { search } = await req.json();
  if (!search) return new Response("Please provide a search param!");
  
  
  // Generate embedding for search term.
  const embedding = await model.run(search, {
    mean_pool: true,
    normalize: true,
  });

  // Query embeddings.
  const queryResponse = await index.namespace(pinecone_namespace).query({
    vector: embedding,
    filter: filter,
    topK: topK,
    includeMetadata: true,
  });

  return Response.json({ search, queryResponse });
});

/* To invoke locally:

  1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
  2. Make an HTTP request:

  curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/search-jerry' \
    --header 'Authorization: Bearer <SUPABASE_ANON_KEY>' \
    --header 'Content-Type: application/json' \
    --data '{"search":"cat"}'

    curl -i --location --request POST 'https://updtdgrdlbtpbksqpilt.supabase.co/functions/v1/search-jerry' \
      --header 'Authorization: Bearer <NEXT_PUBLIC_SUPABASE_ANON_KEY>' \
      --header 'Content-Type: application/json' \
      --data '{"search":"vehicles"}'
  
*/
