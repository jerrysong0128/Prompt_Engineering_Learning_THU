import "https://esm.sh/v135/@supabase/functions-js@2.4.1/src/edge-runtime.d.ts";

import { createClient } from "npm:@supabase/supabase-js@2.42.0";
import { Database } from "../_shared/database.types.ts";

const supabase = createClient<Database>(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

const model = new Supabase.ai.Session("gte-small");

Deno.serve(async (req) => {
  const { search } = await req.json();
  if (!search) return new Response("Please provide a search param!");
  // Generate embedding for search term.
  const embedding = await model.run(search, {
    mean_pool: true,
    normalize: true,
  });

  // Query embeddings.
  const { data: result, error } =  await supabase
    .rpc("query_embeddings", {
      embedding: JSON.stringify(embedding),
      match_threshold: 0.8,
    })
    .select("content")
    .limit(3);
  if (error) {
    return Response.json(error);
  }

  return Response.json({ search, result });
});

/* To invoke locally:

  1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
  2. Run `supabase functions serve`
  3. Make an HTTP request:

  curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/search' \
    --header 'Authorization: Bearer <SUPABASE_ANON_KEY>' \
    --header 'Content-Type: application/json' \
    --data '{"search":"vehicles"}'

   To invoke on the edge:
   
    curl -i --location --request POST 'https://updtdgrdlbtpbksqpilt.supabase.co/functions/v1/search' \
      --header 'Authorization: Bearer <NEXT_PUBLIC_SUPABASE_ANON_KEY>' \
      --header 'Content-Type: application/json' \
      --data '{"search":"vehicles"}'

*/
