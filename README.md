## Overview
Modern operating systems promote virtualization of their underlying machines and isolation using process/thread abstractions. As a result, threads/processes also become the identities of resource scheduling for tasks in the system. However, the "matching" between abstraction and resource allocation also creates "mismatching" between tasks and their real demands of resources. For example, process scheduling is based on the CPU time, regardless their I/O usages. The system also lacks flexibilities in controlling the usage of system resources for threads/processes with different properties as they are all treated the same.

To address the above issue, [resource containers](https://www.usenix.org/legacy/events/osdi99/full_papers/banga/banga.pdf) provide another abstraction other than processes and threads for resource allocation. Each resource container logically abstracts a set of system resources for tasks within the container to use. Depending on the demand of applications, the system can assign different resource containers with different amount of system resources. Each resource container can potentially implement its own scheduling policy to efficiently use its own resources. Recent cloud platforms as well as software engineering platforms further extend the concept of containers to achieve lightweight virtualization and protection among tasks.

As operating systems only supports processes and threads by default, implementing resource containers would require additional efforts in any operating system kernel. Fortunately, most modern operating systems support "loadable kernel modules". In this way, the system can boot with a simpler, smaller kernel and then load these modules into kernel space when necessary. In this project, we will implement resource containers as a loadable kernel module as well as set of library functions that create a pseudo device in the system and provide an interface for applications. By interacting with this device, processes can assign its own threads to difference resource containers.

With this new facilities, threads assigned to the same resource container will/can only share the same set of resources within the container. This semester, you will be gradually building this new facilities in terms of the supports for resource allocations for processors, memory and file storage. In the first project, you will build a kernel module to allocate processor resources and schedule the execution of threads within resource containers.

In this project, you will be given the prototype of the kernel module with a core.c file in its source directory that only contains empty functions. We also provide a user-space library that allows an application to interact with this kernel module through ioctl interfaces as well as a sample benchmark application that you may extend to test if your kernel module functions correctly.

### Kernel Compilation
```shell
cd kernel_module
sudo make
sudo make install
cd ..
```

### User Space Library Compilation
```shell
cd library
sudo make
sudo make install
cd ..
```

### Benchmark Compilation
```shell
cd benchmark
make
cd ..
```

### Run
```shell
./test.sh <num_of_containers> [<num_of_task_for_container1> ...]

# example
./test.sh 1 2
./test.sh 2 2 4
```
## Tasks
1. Implementing the process_container kernel module: it needs the following features:

    - create: you will need to support create operation that creates a container if the corresponding cid hasn't been assigned yet, and assign the task to the container. These create requests are invoked by the user-space library using ioctl interface. The ioctl system call will be redirected to `process_container_ioctl` function located in `src/ioctl.c`

    - delete: you will need to support delete operation that removes tasks from the container. If there is no task in the container, the container should be destroyed as well. These delete requests are invoked by the user-space library using ioctl interface. The ioctl system call will be redirected to `process_container_ioctl` function located in `src/ioctl.c`

    - switch: you will need to support Linux process scheduling mechanism to switch tasks between threads.

    - lock/unlock: you will need to support locking and unlocking that guarantees only one process can access an object at the same time. These lock/unlock functions are invoked by the user-space library using ioctl interface. The ioctl system call will be redirected to `process_container_ioctl` function located in `src/ioctl.c`

2. Test the developed module: It's your responsibility to test the developed kernel module thoroughly. Our benchmark is just a starting point of your testing. The TA/grader will generate a different test sequence to test your program when grading. Your module should support an infinite number of containers and different numbers of tasks with each container.

### Directory Structure
.
├── benchmark
│   ├── benchmark
│   ├── benchmark.c
│   └── Makefile
├── kernel_module
│   ├── 80-process_container.rules
│   ├── COPYING
│   ├── dkms.conf
│   ├── include
│   │   └── processor_container.h
│   ├── interface.c
│   ├── interface.o
│   ├── Kbuild
│   ├── Makefile
│   ├── modules.order
│   ├── Module.symvers
│   ├── processor_container-blacklist.conf
│   ├── processor_container.ko
│   ├── processor_container.mod.c
│   ├── processor_container.mod.o
│   ├── processor_container.o
│   └── src
│       ├── core.c
│       ├── core.o
│       ├── ioctl.c
│       └── ioctl.o
├── library
│   ├── libpcontainer.so.1.0
│   ├── Makefile
│   ├── pcontainer.c
│   ├── pcontainer.h
│   └── pcontainer.o
├── README.md
└── test.sh

## Useful Kernel Functions/Variables
### Mutex
```c
mutex_init(struct mutex *lock);
mutex_lock(struct mutex *lock);
mutex_unlock(struct mutex *lock);
```

### Schedule
```c
// functions
wake_up_process(struct task_struct *p);
set_current_state(volatile long state);
schedule();

// variables
volatile long TASK_INTERRUPTIBLE;
volatile long TASK_RUNNING;
struct task_struct *current;
```

### Memory Allocation
```c
// functions
kmalloc(size_t size, gfp_t flags);
kcalloc(size_t n, size_t size, gfp_t flags);
kfree(const void * objp);

// variables
gfp_t GFP_KERNEL;
```

### Debug Message
```c
// functions
printk(const char *fmt, ...);
```

## References and Hints
1. This project is based on this paper: http://people.cs.uchicago.edu/~shanlu/teaching/33100_fa15/papers/rc-osdi99.pdf, you may need to read it to understand the high-level view of this project.

2. You may also search Linux cgroup, LXC or Docker implementations to get deeper understanding of this project.

3. You should try to figure out the interactions between user-space applications (e.g. benchmark) and the user-space library, the user-space library and the kernel module. You should especially understand how to context switch tasks in the user-space that the functionality is defined in pcontainer_init(), handler(), pcontainer_context_switch_handler() from the user-space library. And you also need to know how to wake up/pause tasks by using wake_up_process()/schedule()/set_current_state(), which are kernel-space functions. Here is the explanation of how to control the status of processes in Linux system: https://www.linuxjournal.com/article/8144

4. You may need to reference the [Linux kernel programming guide](http://www.tldp.org/LDP/lkmpg/2.6/lkmpg.pdf) and [Linux Device Drivers, 3rd Edition](https://lwn.net/Kernel/LDD3/) since user-space libraries will not be available for kernel code.