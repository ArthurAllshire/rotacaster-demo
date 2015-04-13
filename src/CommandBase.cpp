#include "CommandBase.h"
#include "Subsystems/ExampleSubsystem.h"
#include "Commands/Scheduler.h"

// Initialize a single static instance of all of your subsystems to NULL
ExampleSubsystem* CommandBase::examplesubsystem = NULL;
Mpu6050* CommandBase::imu = NULL;
OI* CommandBase::oi = NULL;

CommandBase::CommandBase(char const *name) :Command(name)
{
}

CommandBase::CommandBase() :Command()
{

}

void CommandBase::init()
{
    // Create a single static instance of all of your subsystems. The following
    // line should be repeated for each subsystem in the project.
    examplesubsystem = new ExampleSubsystem();
    imu = new Mpu6050(I2C::kMXP);
    oi = new OI();
}
