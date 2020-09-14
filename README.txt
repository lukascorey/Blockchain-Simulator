How to Run: 
1. run "python honest.py" in terminal 1
2. run "python dishonest.py" in terminal 2
These programs wait for generator.py to be run.
3. run "python generator.py" in terminal 3
4. All three programs will soon print "listening for query" to the terminal. Wait for this to happen. 
5. Run "python joiner.py" in terminal 4

I validate the chain of each at the end just for fun. 

An example output of each program when run correctly is below.



----joiner.py----: 
added nodes
requesting chain
requesting chain
requesting chain

No. of Blocks: 3
        Block 0. 0000cdeda2b313c60f035a45a2addbff2436ec873557b3ca494089e0990b315c
        Block 1. 00008e1f7aece8b0ecfd7f4c40846509e79e4edba5a7390e6da3dae117c4a217
        Block 2. 00004fff666141d7e6b39a07c3aaf73c80cb0c42d6696a4dff611fab80cff0c5


blockchain has been validated

----generator.py----:
block accepted
listening for honest
block accepted
listening for dishonest
block rejected
listening for honest2
block accepted
listening for query
got message: requesting chain

No. of Blocks: 3
        Block 0. 0000cdeda2b313c60f035a45a2addbff2436ec873557b3ca494089e0990b315c
        Block 1. 00008e1f7aece8b0ecfd7f4c40846509e79e4edba5a7390e6da3dae117c4a217
        Block 2. 00004fff666141d7e6b39a07c3aaf73c80cb0c42d6696a4dff611fab80cff0c5


blockchain has been validated

----honest.py----: 
block accepted
got genesis
block accepted
broadcast new honest block
block rejected
should have ignored dishonest block
block accepted
broadcast new honest block
listening for query
got message: requesting chain

No. of Blocks: 3
        Block 0. 0000cdeda2b313c60f035a45a2addbff2436ec873557b3ca494089e0990b315c
        Block 1. 00008e1f7aece8b0ecfd7f4c40846509e79e4edba5a7390e6da3dae117c4a217
        Block 2. 00004fff666141d7e6b39a07c3aaf73c80cb0c42d6696a4dff611fab80cff0c5


blockchain has been validated

----dishonest.py----:
block accepted
although block accepted and valid, it is ignored
block accepted
block rejected
listening for query
got message: requesting chain

No. of Blocks: 2
        Block 0. 0000cdeda2b313c60f035a45a2addbff2436ec873557b3ca494089e0990b315c
        Block 1. 0000fcc3ef224d96d3fd967caedfe529d8331b2a9d468f74313562cc990a3364


blockchain has been validated