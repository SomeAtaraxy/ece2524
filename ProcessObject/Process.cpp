#include "Process.h"

/* Initialize the process, create input/output pipes */
Process::Process(const std::vector<std::string> &args)
{
    int errCheck1 = pipe(readpipe);
    int errCheck2 = pipe(writepipe);
    if(errCheck1 < 0 || errCheck2 < 0)
    {
        std::cerr << "Error with pipe(): " << strerror(errno) << std::endl;
        exit(0);
    }



    if((m_pid = fork()) < 0)
    {
        // there was an error forking
        std::cerr << "Error with fork(): " << strerror(errno) << std::endl;
        exit(0);
    }
    else if (m_pid == 0)
    {
        // Child
        errCheck1 = errCheck2 = 0;
        errCheck1 = dup2(readpipe[1],1);
        errCheck2 = dup2(writepipe[0],0);
        if(errCheck1 < 0 || errCheck2 < 0)
        {
            std::cerr << "Error with dup2(): " << strerror(errno) << std::endl;
            exit(0);
        }

        errCheck1 = errCheck2 = 0;
        errCheck1 = close(readpipe[1]);
        errCheck2 = close(readpipe[0]);
        if(errCheck1 < 0 || errCheck2 < 0)
        {
            std::cerr << "Error with close(readpipe): " << strerror(errno) << std::endl;
            exit(0);
        }

        errCheck1 = errCheck2 = 0;
        errCheck1 = close(writepipe[1]);
        errCheck2 = close(writepipe[0]);
        if(errCheck1 < 0 || errCheck2 < 0)
        {
            std::cerr << "Error with close(writepipe): " << strerror(errno) << std::endl;
            exit(0);
        }

        std::vector<const char*> cargs;
        std::transform(args.begin(), args.end(), std::back_inserter(cargs),
                [](const std::string s){return &s[0];});
        cargs.push_back(NULL);

        char *charNULL[] = {(char*)0};
        if(-1 == execve(const_cast<char*>(cargs[0]), charNULL, charNULL))
        {
            std::cerr << "Error with execve(): " << strerror(errno) << std::endl;
            exit(0);
        }

    }
    else
    {
        // Parent
        std::cout << "Parent[" << getpid() << "] Process constructor" << std::endl;

        errCheck1 = errCheck2 = 0;
        errCheck1 = close(writepipe[0]);
        errCheck2 = close(readpipe[1]);
        if(errCheck1 < 0)
        {
            std::cerr << "Error with close(writepipe): " << strerror(errno) << std::endl;
            exit(0);
        }
        else if(errCheck2 < 0)
        {
            std::cerr << "Error with close(readpipe): " << strerror(errno) << std::endl;
            exit(0);
        }

        m_pread = fdopen(readpipe[0], "r");
    }
}

/* Close any open file streams or file descriptors,
   insure that the child has terminated */
Process::~Process()
{
    close(writepipe[1]);
    close(readpipe[0]);

    fclose(m_pread);
}

/* write a string to the child process */
void Process::write(const std::string output)
{
    ::write(writepipe[1], output.c_str(), output.size());
}

/* read a full line from child process,
   if no line is available, block until one becomes available */
std::string Process::readline()
{
    char* readptr;
    std::string output;
    size_t n = 100;
    ssize_t length = 0;

    readptr = (char*) malloc (n + 1);
    length = getline(&readptr, &n, m_pread);

    if(length == -1)
    {
        std::cerr << "Error with getline(): " <<strerror(errno) << std::endl;
        //exit(0);
    }

    for(int i=0; i<length; i++)
        output += readptr[i];

    return output;
}
