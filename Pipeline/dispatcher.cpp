/*
 * Collin Schumann
 * ECE 2524
 * Assignment: Heard it on the pipeline
*/

#include <unistd.h>
#include <stdio.h>
#include <iostream>
#include <sys/wait.h>

int main()
{
    char *args[] = {(char*)0};

    int genToCons[2]; //Generator will write to pwrite[1]
    pipe(genToCons);

    pid_t childGen, childCons;


    if((childGen = fork()) < 0)
    {
        // there was an error forking
        perror("fork Generator");
    }
    else if (childGen == 0)
    {
        // Generator child code

        dup2(genToCons[1],1);

        close(genToCons[1]);
        close(genToCons[0]);

        if ( -1 == execve("./generator", args, args) )
        {
            perror("Error calling execpe");
            _exit(0);
        }
    }
    else
    {
        if((childCons = fork()) < 0)
        {
            // there was an error forking
            perror("fork Consumer");
        }
        else if (childCons == 0)
        {
            // Consumer child code

            dup2(genToCons[0],0);

            close(genToCons[1]);
            close(genToCons[0]);

            if ( -1 == execve("./consumer", args, args) )
            {
                perror("Error calling execpe");
                _exit(0);
            }
        }
        else
        {
            // Parent Code
            close(genToCons[1]);
            close(genToCons[0]);

            sleep(1);

            kill(childGen, SIGTERM);
            int status;
            waitpid(childGen, &status, 0);
            std::cerr << "Parent waited for child[" << childGen << "] to exit with status " << status << std::endl;

            waitpid(childCons, &status, 0);
            std::cerr << "Parent waited for child[" << childCons << "] to exit with status " << status << std::endl;
        }
    }
}
