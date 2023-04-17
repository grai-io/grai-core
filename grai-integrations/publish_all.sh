#! bash


for i in $(ls -d */ | grep source); do
  cd ./${i}
  poetry publish --build
  cd ..
done
