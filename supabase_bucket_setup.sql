-- Supabase Storage policies for bucket PDC
-- Run this in the Supabase SQL Editor

-- Allow public reads from the bucket
drop policy if exists "Public read PDC" on storage.objects;

create policy "Public read PDC"
on storage.objects
for select
to public
using (bucket_id = 'PDC');

-- Allow anonymous inserts so the lab can upload files
drop policy if exists "Anon insert PDC" on storage.objects;

create policy "Anon insert PDC"
on storage.objects
for insert
to anon
with check (bucket_id = 'PDC');
