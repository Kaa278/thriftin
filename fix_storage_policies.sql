-- Hapus semua policy lama yang spesifik ke role (anon/authenticated)
drop policy if exists "allow anon product image reads" on storage.objects;
drop policy if exists "allow anon product image uploads" on storage.objects;
drop policy if exists "allow anon product image updates" on storage.objects;
drop policy if exists "allow anon product image deletes" on storage.objects;
drop policy if exists "allow anon profile photo reads" on storage.objects;
drop policy if exists "allow anon profile photo uploads" on storage.objects;
drop policy if exists "allow anon profile photo updates" on storage.objects;
drop policy if exists "allow anon profile photo deletes" on storage.objects;
drop policy if exists "allow authenticated product image reads" on storage.objects;
drop policy if exists "allow authenticated product image uploads" on storage.objects;
drop policy if exists "allow authenticated product image updates" on storage.objects;
drop policy if exists "allow authenticated product image deletes" on storage.objects;
drop policy if exists "allow authenticated profile photo reads" on storage.objects;
drop policy if exists "allow authenticated profile photo uploads" on storage.objects;
drop policy if exists "allow authenticated profile photo updates" on storage.objects;
drop policy if exists "allow authenticated profile photo deletes" on storage.objects;

-- Buat policy baru yang berlaku untuk SEMUA operasi (SELECT, INSERT, UPDATE, DELETE)
-- dan untuk SEMUA role (public, anon, authenticated)
create policy "allow all product image operations" 
  on storage.objects for all 
  using (bucket_id = 'product-images');

create policy "allow all profile photo operations" 
  on storage.objects for all 
  using (bucket_id = 'profile-photos');
