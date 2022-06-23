import { createClient } from '@supabase/supabase-js'

// Create a single supabase client for interacting with your database
// const supabaseUrl = process.env.REACT_APP_SUPABASE_URL
// const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY
const supabaseUrl = "https://jjzktuzgznsnbdfrcmqq.supabase.co"
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTY0MzMyMDA5NSwiZXhwIjoxOTU4ODk2MDk1fQ.1_tKrvgnDFEYZFmK_j4NcSDXTX5cPCGbRiY6rboh5Gs"

export const supabase = createClient(supabaseUrl, supabaseAnonKey)